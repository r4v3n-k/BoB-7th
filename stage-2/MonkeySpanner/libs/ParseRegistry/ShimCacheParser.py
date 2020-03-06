import logging
import struct
import datetime

from modules.constant import REGISTRY_KEYWORD
# Values used by Windows 6.1 (Win7 and Server 2008 R2)
CACHE_MAGIC_NT6_1 = 0xbadc0fee
CACHE_HEADER_SIZE_NT6_1 = 0x80
NT6_1_ENTRY_SIZE32 = 0x20
NT6_1_ENTRY_SIZE64 = 0x30
CSRSS_FLAG = 0x2

# Values used by Windows 10
WIN10_STATS_SIZE = 0x30
WIN10_CREATORS_STATS_SIZE = 0x34
WIN10_MAGIC = '10ts'
CACHE_HEADER_SIZE_NT6_4 = 0x30
CACHE_MAGIC_NT6_4 = 0x30

bad_entry_data = 'N/A'
g_verbose = False
g_usebom = False
output_header  = ["Last Modified", "Last Update", "Path", "File Size", "Exec Flag"]

# Date Formats
DATE_MDY = "%m/%d/%y %H:%M:%S"
DATE_ISO = "%Y-%m-%d %H:%M:%S.%f"
g_timeformat = DATE_ISO

g_timeline = None
grayHead = [REGISTRY_KEYWORD, True, 0, 0, 0, 0, 0, 0]
# Shim Cache format used by Windows 6.1 (Win7 through Server 2008 R2)
class CacheEntryNt6(object):

	def __init__(self, is32bit, data=None):

		self.is32bit = is32bit
		if data != None:
			self.update(data)

	def update(self, data):
		if self.is32bit:
			entry = struct.unpack('<2H 7L', data)
		else:
			entry = struct.unpack('<2H 4x Q 4L 2Q', data)
		self.wLength = entry[0]
		self.wMaximumLength =  entry[1]
		self.Offset = entry[2]
		self.dwLowDateTime = entry[3]
		self.dwHighDateTime = entry[4]
		self.FileFlags = entry[5]
		self.Flags = entry[6]
		self.BlobSize = entry[7]
		self.BlobOffset = entry[8]

	def size(self):

		if self.is32bit:
			return NT6_1_ENTRY_SIZE32
		else:
			return NT6_1_ENTRY_SIZE64

# Convert FILETIME to datetime.
# Based on http://code.activestate.com/recipes/511425-filetime-to-datetime/
def convert_filetime(dwLowDateTime, dwHighDateTime):
	global g_timeline
	try:
		date = datetime.datetime(1601, 1, 1, 0, 0, 0)
		temp_time = dwHighDateTime
		temp_time <<= 32
		temp_time |= dwLowDateTime
		res = date + datetime.timedelta(microseconds=temp_time/10)
		if g_timeline:
			if res < g_timeline:
				return None
		return res
	except OverflowError as err:
		logging.info("[Error] AppCompatCache: {}".format(err))
		return None

# Return a unique list while preserving ordering.
def unique_list(li):

	ret_list = []
	for entry in li:
		if entry not in ret_list:
			ret_list.append(entry)
	return ret_list

# Read Windows 10 Apphelp Cache entry format
def read_win10_entries(bin_data, ver_magic, creators_update=False):
	try:
		offset = 0
		entry_meta_len = 12
		entry_list = []

		# Skip past the stats in the header
		if creators_update:
			cache_data = bin_data[WIN10_CREATORS_STATS_SIZE:]
		else:
			cache_data = bin_data[WIN10_STATS_SIZE:]

		from io import BytesIO
		data = BytesIO(cache_data)
		while data.tell() < len(cache_data):
			header = data.read(entry_meta_len)
			# Read in the entry metadata
			# Note: the crc32 hash is of the cache entry data
			magic, crc32_hash, entry_len = struct.unpack('<4sLL', header)
			magic = magic.decode()

			# Check the magic tag
			if magic != ver_magic:
				raise Exception("Invalid version magic tag found: 0x%x" % struct.unpack("<L", magic)[0])

			entry_data = BytesIO(data.read(entry_len))

			# Read the path length
			path_len = struct.unpack('<H', entry_data.read(2))[0]
			if path_len == 0:
				path = 'None'
			else:
				path = entry_data.read(path_len).decode('utf-16le', 'replace')

				from modules.constant import SYSTEMROOT, LOCALAPPDATA
				if path[-3:].lower() != "exe":
					if SYSTEMROOT.lower() not in path.lower() and LOCALAPPDATA not in path.lower():
						continue

			# Read the remaining entry data
			low_datetime, high_datetime = struct.unpack('<LL', entry_data.read(8))

			last_mod_date = convert_filetime(low_datetime, high_datetime)
			if not last_mod_date:
				continue
			try:
				last_mod_date = last_mod_date.strftime("%Y-%m-%d %H:%M:%S.%f")
			except ValueError as e:
				logging.info('[Error] AppCompatCache: {}'.format(e))
				continue

			row = [grayHead, last_mod_date, path, 'N/A', 'N/A', "AppCompatCache"]

			if row not in entry_list:
				entry_list.append(row)
		g_timeline = None
		return entry_list
	except (RuntimeError, ValueError, NameError) as err:
		logging.info('[Error] reading Shim Cache data: {}...'.format(err))
		g_timeline = None
		return None

# Read the Shim Cache Windows 7/2k8-R2 entry format,
# return a list of last modifed dates/paths.
def read_nt6_entries(bin_data, entry):

	try:
		entry_list = []
		exec_flag = ""
		entry_size = entry.size()
		num_entries = struct.unpack('<L', bin_data[4:8])[0]
		
		if num_entries == 0:
			return None
		# Walk each entry in the data structure.
		for offset in range(CACHE_HEADER_SIZE_NT6_1,
							 num_entries*entry_size + CACHE_HEADER_SIZE_NT6_1,
							 entry_size):

			entry.update(bin_data[offset:offset+entry_size])
			last_mod_date = convert_filetime(entry.dwLowDateTime,
											 entry.dwHighDateTime)
			if not last_mod_date:
				continue
			try:
				last_mod_date = last_mod_date.strftime("%Y-%m-%d %H:%M:%S.%f")
			except ValueError as e:
				logging.info('[Error] AppCompatCache: {}'.format(e))
				continue
			path = (bin_data.decode("unicode-escape")[entry.Offset:entry.Offset +
							 entry.wLength])[8:].replace("\x00", "")
			from modules.constant import SYSTEMROOT, LOCALAPPDATA
			if path[-3:].lower() != "exe":
				if SYSTEMROOT.lower() not in path.lower() and LOCALAPPDATA not in path.lower():
					continue

			if (entry.FileFlags & CSRSS_FLAG):
				exec_flag = 'True'
			else:
				exec_flag = 'False'

			row = [grayHead, last_mod_date, path, 'N/A', exec_flag, "AppCompatCache"]

			if row not in entry_list:
				entry_list.append(row)
		g_timeline = None
		return entry_list

	except (RuntimeError, ValueError, NameError) as err:
		logging.info('[Error] reading Shim Cache data: {}...'.format(err))
		g_timeline = None
		return None

def read_cache(cachebin, quiet=False, timeline=None):
	global g_timeline
	g_timeline = timeline

	if len(cachebin) < 16:
		return None

	try:
		magic = struct.unpack("<L", cachebin[:4])[0]
		# This is a Windows 7/2k8-R2 Shim Cache.
		if magic == CACHE_MAGIC_NT6_1:
			test_size = (struct.unpack("<H",
						 cachebin[CACHE_HEADER_SIZE_NT6_1:
						 CACHE_HEADER_SIZE_NT6_1 + 2])[0])
			test_max_size = (struct.unpack("<H", cachebin[CACHE_HEADER_SIZE_NT6_1+2:
							 CACHE_HEADER_SIZE_NT6_1 + 4])[0])

			if (test_max_size-test_size == 2 and
				struct.unpack("<L", cachebin[CACHE_HEADER_SIZE_NT6_1+4:
				CACHE_HEADER_SIZE_NT6_1 + 8])[0] ) == 0:
				if not quiet:
					logging.info("[+] Found 64bit Windows 7/2k8-R2 Shim Cache data...")
				entry = CacheEntryNt6(False)
				return read_nt6_entries(cachebin, entry)
			else:
				if not quiet:
					logging.info("[+] Found 32bit Windows 7/2k8-R2 Shim Cache data...")
				entry = CacheEntryNt6(True)
				return read_nt6_entries(cachebin, entry)

		# Windows 10 will use a different magic dword, check for it
		elif len(cachebin) > WIN10_STATS_SIZE and cachebin[WIN10_STATS_SIZE:WIN10_STATS_SIZE+4].decode() == WIN10_MAGIC:
			if not quiet:
				logging.info("[+] Found Windows 10 Apphelp Cache data...")
			return read_win10_entries(cachebin, WIN10_MAGIC)

		# Windows 10 Creators Update will use a different STATS_SIZE, account for it
		elif len(cachebin) > WIN10_CREATORS_STATS_SIZE and cachebin[WIN10_CREATORS_STATS_SIZE:WIN10_CREATORS_STATS_SIZE+4].decode() == WIN10_MAGIC:
			if not quiet:
				logging.info("[+] Found Windows 10 Creators Update Apphelp Cache data...")
			return read_win10_entries(cachebin, WIN10_MAGIC, creators_update=True)

		else:
			logging.info('[Error] AppCompatCache: Got an unrecognized magic value of 0x%x... bailing' % magic)
			g_timeline = None
			return None

	except (RuntimeError, TypeError, NameError) as err:
		logging.info('[Error] reading Shim Cache data: {}'.format(err))
		g_timeline = None
		return None
