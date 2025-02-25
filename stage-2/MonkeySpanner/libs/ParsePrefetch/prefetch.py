import binascii
import ctypes
from datetime import datetime, timedelta
import ntpath
import struct
import sys
import tempfile

class Prefetch(object):
	def __init__(self, infile):
		self.pFileName = infile

		with open(infile, "rb") as f:
			if f.read(3).decode() == "MAM":
				f.close()

				d = DecompressWin10()
				decompressed = d.decompress(infile)
				
				t = tempfile.mkstemp()
				
				with open(t[1], "wb+") as f:
					f.write(decompressed)
					f.seek(0)

					self.parseHeader(f)
					self.fileInformation26(f)
					self.metricsArray23(f)
					self.traceChainsArray30(f)
					self.volumeInformation30(f)
					self.getTimeStamps(self.lastRunTime)
					self.directoryStrings(f)
					self.getFilenameStrings(f)
					return

		with open(infile, "rb") as f:
			self.parseHeader(f)

			if self.version == 17:
				print("self.version: "+str(self.version))
			
			elif self.version == 23:
				self.fileInformation23(f)
				self.metricsArray23(f)
				self.traceChainsArray17(f)
				self.volumeInformation23(f)
				self.getTimeStamps(self.lastRunTime)
				self.directoryStrings(f)

			elif self.version == 26:
				print("self.version: "+str(self.version))

			self.getFilenameStrings(f)

	def parseHeader(self, infile):
		# Parse the file header
		# 84 bytes
		self.version = struct.unpack_from("I", infile.read(4))[0]
		self.signature = struct.unpack_from("I", infile.read(4))[0]
		unknown0 = struct.unpack_from("I", infile.read(4))[0]
		self.fileSize = struct.unpack_from("I", infile.read(4))[0]
		executableName = struct.unpack_from("60s", infile.read(60))[0]
		executableName = executableName.decode("unicode-escape").split("\x00\x00")[0]
		self.executableName = executableName.replace("\x00", "")
		rawhash = hex(struct.unpack_from("I", infile.read(4))[0])
		self.hash = rawhash.lstrip("0x")
		unknown1 = infile.read(4).decode("unicode-escape")

	def traceChainsArray17(self, infile):
		# Read through the Trace Chains Array
		# Not being parsed for information
		# 12 bytes
		infile.read(12)

	def fileInformation23(self, infile):
		# File Information
		# 156 bytes
		self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
		self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
		self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
		self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
		self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
		self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
		unknown0 = infile.read(8).decode("unicode-escape")
		self.lastRunTime = infile.read(8)
		unknown1 = infile.read(16).decode("unicode-escape")
		self.runCount = struct.unpack_from("I", infile.read(4))[0]
		unknown2 = infile.read(84).decode("unicode-escape")

	def metricsArray23(self, infile):
		# File Metrics Array
		# 32 bytes per array, not parsed in this script
		infile.seek(self.metricsOffset)
		unknown0 = infile.read(4)
		unknown1 = infile.read(4)
		unknown2 = infile.read(4)
		self.filenameOffset = struct.unpack_from("I", infile.read(4))[0]
		self.filenameLength = struct.unpack_from("I", infile.read(4))[0]
		unknown3 = infile.read(4)
		self.mftRecordNumber = self.convertFileReference(infile.read(6).decode("unicode-escape"))
		self.mftSeqNumber = struct.unpack_from("H", infile.read(2))[0]
		
	def volumeInformation23(self, infile):
		# This function consumes the Volume Information array
		# 104 bytes per structure in the array
		# Returns a dictionary object which holds another dictionary
		# for each volume information array entry

		infile.seek(self.volumesInformationOffset)
		self.volumesInformationArray = []
		self.directoryStringsArray = []
		
		count = 0
		while count < self.volumesCount:
			self.volPathOffset = struct.unpack_from("I", infile.read(4))[0]
			self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
			self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
			volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
			self.volSerialNumber = volSerialNumber.rstrip("L").lstrip("0x")
			self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
			self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
			self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
			self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
			unknown0 = infile.read(68)

			self.directoryStringsArray.append(self.directoryStrings(infile))
			
			infile.seek(self.volumesInformationOffset + self.volPathOffset)
			volume = {}
			volume["Volume Name"] = infile.read(self.volPathLength * 2).decode("unicode-escape").replace("\x00", "")
			volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
			volume["Serial Number"] = self.volSerialNumber
			self.volumesInformationArray.append(volume)
			
			count += 1
			infile.seek(self.volumesInformationOffset + (104 * count))
			

	def fileInformation26(self, infile):
		# File Information
		# 224 bytes
		self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
		self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
		self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
		self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
		self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
		self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
		self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
		unknown0 = infile.read(8)
		self.lastRunTime = infile.read(64)
		unknown1 = infile.read(16)
		self.runCount = struct.unpack_from("I", infile.read(4))[0]
		unknown2 = infile.read(96)

	def traceChainsArray30(self, infile):
		# Trace Chains Array
		# Read though, not being parsed for information
		# 8 bytes
		infile.read(8)

	def volumeInformation30(self, infile):
		# Volumes Information
		# 96 bytes

		infile.seek(self.volumesInformationOffset)
		self.volumesInformationArray = []
		self.directoryStringsArray = []

		count = 0
		while count < self.volumesCount:
			self.volPathOffset = struct.unpack_from("I", infile.read(4))[0] 
			self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
			self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
			self.volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
			self.volSerialNumber = self.volSerialNumber.rstrip("L").lstrip("0x")
			self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
			self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
			self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
			self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
			unknown0 = infile.read(60)

			self.directoryStringsArray.append(self.directoryStrings(infile))

			infile.seek(self.volumesInformationOffset + self.volPathOffset)
			volume = {}
			volume["Volume Name"] = infile.read(self.volPathLength * 2).decode("unicode-escape").replace("\x00", "")
			volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
			volume["Serial Number"] = self.volSerialNumber
			self.volumesInformationArray.append(volume)
			
			count += 1
			infile.seek(self.volumesInformationOffset + (96 * count))

	def getFilenameStrings(self, infile):
		# Parses filename strings from the PF file
		self.resources = []
		infile.seek(self.filenameStringsOffset)
		self.filenames = infile.read(self.filenameStringsSize).decode("utf-16")
		
		# for i in self.filenames.split("\x00\x00"):
		for i in self.filenames.split("\x00"):
			self.resources.append(i.replace("\x00", ""))

	def convertTimestamp(self, timestamp):
		# Timestamp is a Win32 FILETIME value
		# This function returns that value in a human-readable format
		return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))


	def getTimeStamps(self, lastRunTime):
		self.timestamps = []

		start = 0
		end = 8
		while end <= len(lastRunTime):
			timestamp = struct.unpack_from("Q", lastRunTime[start:end])[0]

			if timestamp:
				self.timestamps.append(self.convertTimestamp(timestamp))
				start += 8
				end += 8
			else:
				break

	def directoryStrings(self, infile):
		infile.seek(self.volumesInformationOffset)
		infile.seek(self.dirStringsOffset, 1)

		directoryStrings = []

		count = 0
		while count < self.dirStringsCount:
			stringLength = struct.unpack_from("<H", infile.read(2))[0] * 2
			# directoryString = infile.read(stringLength).decode("unicode-escape").replace("\x00", "")
			directoryString = infile.read(stringLength).decode('utf-16')
			infile.read(2) # Read through the end-of-string null byte
			directoryStrings.append(directoryString)
			count += 1
		
		return directoryStrings

	def convertFileReference(self, buf):
		byteArray = list(map(lambda x: '%02x' % ord(x), buf))
			
		byteString = ""
		for i in byteArray[::-1]:
			byteString += i
		
		return int(byteString, 16)


	def getContents(self):
		contents = [
			ntpath.basename(self.pFileName),
			[self.executableName, str(self.runCount)],
			[str(self.mftRecordNumber), str(self.mftSeqNumber)],
		]

		total = len(self.timestamps) - 1
		contents.append(["{}".format(self.timestamps[i]) for i in range(total, -1, -1)])

		for i in self.volumesInformationArray:
			contents.append([
				i["Volume Name"], "{}".format(i['Creation Date']), "{}".format(i["Serial Number"])
			])

		dirStrList = []
		for volume in self.directoryStringsArray:
			for i in volume:
				dirStrList.append("{}".format(i))
		contents.append(dirStrList)
		contents.append([rsc for rsc in self.resources if rsc])
		return contents

class DecompressWin10(object):
	def __init__(self):
		pass

	def tohex(self, val, nbits):
		"""Utility to convert (signed) integer to hex."""
		return hex((val + (1 << nbits)) % (1 << nbits))

	def decompress(self, infile):
		"""Utility core."""

		NULL = ctypes.POINTER(ctypes.c_uint)()
		SIZE_T = ctypes.c_uint
		DWORD = ctypes.c_uint32
		USHORT = ctypes.c_uint16
		UCHAR  = ctypes.c_ubyte
		ULONG = ctypes.c_uint32

		# You must have at least Windows 8, or it should fail.
		try:
			RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
		except AttributeError as e:
			sys.exit("[ - ] {}".format(e) + \
			"\n[ - ] Windows 8+ required for this script to decompress Win10 Prefetch files")

		RtlGetCompressionWorkSpaceSize = \
			ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

		with open(infile, 'rb') as fin:
			header = fin.read(8)
			compressed = fin.read()

			signature, decompressed_size = struct.unpack('<LL', header)
			calgo = (signature & 0x0F000000) >> 24
			crcck = (signature & 0xF0000000) >> 28
			magic = signature & 0x00FFFFFF
			if magic != 0x004d414d :
				sys.exit('Wrong signature... wrong file?')

			if crcck:
				# I could have used RtlComputeCrc32.
				file_crc = struct.unpack('<L', compressed[:4])[0]
				crc = binascii.crc32(header)
				crc = binascii.crc32(struct.pack('<L',0), crc)
				compressed = compressed[4:]
				crc = binascii.crc32(compressed, crc)		  
				if crc != file_crc:
					sys.exit('{} Wrong file CRC {0:x} - {1:x}!'.format(infile, crc, file_crc))

			compressed_size = len(compressed)

			ntCompressBufferWorkSpaceSize = ULONG()
			ntCompressFragmentWorkSpaceSize = ULONG()

			ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
				ctypes.byref(ntCompressBufferWorkSpaceSize),
				ctypes.byref(ntCompressFragmentWorkSpaceSize))

			if ntstatus:
				sys.exit('Cannot get workspace size, err: {}'.format(
					self.tohex(ntstatus, 32)))
					
			ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
			ntDecompressed = (UCHAR * decompressed_size)()
			ntFinalUncompressedSize = ULONG()
			ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()
			
			ntstatus = RtlDecompressBufferEx(
				USHORT(calgo),
				ctypes.byref(ntDecompressed),
				ULONG(decompressed_size),
				ctypes.byref(ntCompressed),
				ULONG(compressed_size),
				ctypes.byref(ntFinalUncompressedSize),
				ctypes.byref(ntWorkspace))

			if ntstatus:
				sys.exit('Decompression failed, err: {}'.format(self.tohex(ntstatus, 32)))

			if ntFinalUncompressedSize.value != decompressed_size:
				sys.exit('Decompressed with a different size than original!')

		return bytearray(ntDecompressed)

def convertTimestamp(timestamp):
		return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))
