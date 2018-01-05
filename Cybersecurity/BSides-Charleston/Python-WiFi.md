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

## Demo

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


