# My Airodump

It is a network scan tool made with reference to [Airodump-ng](https://www.aircrack-ng.org/doku.php?id=airodump-ng). The tool was written with Qt5, so It has GUI and improved what I thought it is inconvenient of the existing.

`Airodump-ng` separately shows Information of an Access Point and a Station. So, a user should catch the MAC address of an Access Point from Stations while data is fast on the screen. In my opinion, it's less convenient in the visual.

To get better, I used the **map** library to implement the connection of several Stations and an Access Point. At first, hopping channels of a wireless network, catching packets and parsing them. And then creating AccessPoint or FakeAccessPoint or Station Object depending on a type of the packet. FakeAccessPoint Object is for a Station not finding the connected Access Point. Anyway, Station object has a member variable, probe, meaning ESSID of the connected Access Point. And an Access Point use the map library to save the connected Stations. With this, an Access Point has several Stations on the screen. Also, MonitorWidget object use the map to search an Access Point by either SSID or MAC address.

``` C++
// accesspoint.h
map<string, Station *> station_map;
```

``` C++
// monitorwidget.h
FakeAccessPoint *not_assoc;
map<string, AccessPoint *> ap_map_by_mac;
map<string, AccessPoint *> ap_map_by_ssid;
```

![1](./1.png?raw=true)

- wlx88366cf83612 is SSID of a USB adapter, ipTime, which supports Monitor Mode.

![2](./2.png?raw=true)

- Green Color is of Access Points.
- White Color is of Stations.

I referred to [IEEE 802.11 Pocket Reference Guide](https://www.willhackforsushi.com/papers/80211_Pocket_Reference_Guide.pdf) for packet analysis and open-source [Airodump-ng](https://github.com/aircrack-ng/aircrack-ng/tree/master/src/airodump-ng)

Finally, if you wanna demo video, visit [here](https://drive.google.com/open?id=1fbHPsbR8MjIQkSFfSypQ9-A678Ofgg0o).

Thank you for reading :)