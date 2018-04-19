Noemi Glaeser  
BSides Charleston  
26-Dec-2017  

# BSides Charleston: Python+WiFi Workshop
**10-Nov-2017  
Speaker: stryngs**

## Tools
- *tmux*: Terminal multiplexer
  - Ctrl-B
  - X to kill panes
- *iPython*
  - `f = []`
  - `f.` + `tab` (to learn more)
  - `f?`

---

## 802.11
Shared Medium

fromDS (destination, BSSID, source)
toDS (destination, BSSID, source)
*1* - toDS
*2* - fromDS
*65* - to DS with encryption
*66* - from DS with encryption

Mnemonic: "it's better TO give than to deceive"

#### Types
*0* - management frame
*1* - control
*2* - data

Mnemonic: M-C-D (McD)

FCfield, addr1-2-3, type

---

## TCP-IP
syn, syn/ack, ack (acknowledgement)
sequence + length = ack (first to respond wins)

#### Flags
FIN
URG
CWR
ACK
SYN
PSH
ECE
RST

Mnemonic: F U Casper

TCP numbers: relative vs. absolute
(Numbers are relative in Wireshark unless you turn on absolute mode)

---

## Cookies
HTTP is stateless, so cookies are used to track the state. Getting the cookie means ACCESS!

---

## Demos

`airmon-ng start wlan1` (drop into air monitor mode)  
`wilist wlan1mon channel` (to show channels and current channel)
`iwconfig wlan1mon channel 6` (to change channels)
`ngrep -d wlan1mon`

#### Scapy
Scapy is an interactive packet manipulator.  
Commands:
- `ls()`
- `lsc()`
- `pkt.show()`
- `rdpcap()`/`wrpcap()`
- `PcapReader()`/`PcapWriter()`
- `hexstr(str(p[0]))` - read in hex
- `hexstr(str(p[0]), onlyasc=1)` or `onlyhex=1`

#### Kate
Useful text editor.

#### Demo 1
`Demos/demo-1.py`

```
# 802.11w spec
aPkts = sniff(iface = iFace, prn = lambda x : x.summary(), lfilter = pHandler, count = 4);

q = Dot11()/TCP()/IP()/RadioTap()
q.summary() # is Dot11()/TCP()

del q.payload.payload # deletes IP & any children

t1 = RadioTap | Dot11 | Dot11AssoReq | Dot11Elt | Dot11Elt | dot11Elt
# t1[RadioTap] gives RadioTap and all children, aka all of t1
# t1[Dot11] only gives Dot11 | Dot11AssoReq | Dot11Elt | Dot11Elt | Dot11Elt
# t1[Dot11Elt] gives Dot11Elt | Dot11Elt

t1[Dot11Elt][Dot11Elt]

f = list(layerYield(t1))
f
```

#### Demo 2
In scapy, `prn` can do `lfilter` stuff and vice versa, but you should filter with `lfilter` and actually do stuff with `prn`.
```
def macFinder(myMac) # only pass packets if one of their addresses is myMac
```

You can substitute lambda for closure
```
lambda x : x[Dot11].addr1 == myMac # ...
```

#### Demo 3
MAC address determines DHCP IP requested:
```
sendp(dhcpReq, inter=1, iface="wlan0mon", count=1000)

dhcpReq[DHCP].options[2] = ('hostname', 'foo')
wireshark(dhcpReq)
```

We have a problem: length is 328, which exceeds 324. So we change the length:
```
del dhcpReq[DHCP].len
wireshark(dhcpReq)
```

Do the same thing checking for problems with checksum or UDP length.
Another possible problem: FCS problem (in the hex at the end of the packet).

#### PyDot11
With WEP, everyone has the same password _and_ packets are the same for everyone. In WPA2, even though everyone uses the same password, the packets are different for different people.
```
.pyDot11 -i wlan0mon -b 'C4:3D:C7:47:B4:4A' -p 'PASSWORD' -t wpa -e 'WPA2'
cat prog_walks | nc termbin.com 9999 # gives http://termbin.com/k0g3
```

Another fun tool (but be smart about how you use it or your could go to jail!!): airpwn-ng.


