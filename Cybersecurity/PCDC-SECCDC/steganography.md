# Steganography

## Tools

* General
    * Unix `file`
    * unzipping into source XML
* Steganography
    * [stegsolve](https://www.wechall.net/forum/show/thread/527/Stegsolve_1.3/page-1)
* Metadata
    * exif

## Examples

Files to practice on can be found in [this Google Drive folder](https://drive.google.com/open?id=13JZdOmNhdDKO-Ta8wzMGndS_34b_EjSI).

Try your hand at them first. Solutions are discussed below.

### Steg1

- Open in stegsolve 
- Click arrows on the bottom until you get to "red plane 0"
- Flag: **SKY-INSI-7918**

### Steg2

**I haven't solved this yet -- please contact me if you figure it out!**

### Salesman

- Open in stegsolve
- Analyze > File Format > Scroll to the bottom
    - Notice that there is more stuff after "End of Image":
```
Additional bytes at end of file = 52  
Dump of additional bytes: 
Hex:
6447677863313969 4e474a3558324d30
626c396d4d585266 637a42666258566a
6146396a636e6c77 644442664d573566
4d58513d 
Ascii:
dGgxc19iNGJ5X2M0bl9mMXRfczBfbXVjaF9jcnlwdDBfMW5fMXQ=
```
- Use [base64decode.org](https://base64decode.org) or the command line to decode the base64-encoded string:
```
echo "dGgxc19i NGJ5X2M0 bl9mMXRf czBfbXVj aF9jcnlw dDBfMW5f MXQ=" | base64 -D
```
- Flag: **th1s\_b4by\_c4n\_f1t\_s0\_much\_crypt0\_1n\_1t**

### Nothing 2 see

**I haven't solved this yet -- please contact me if you figure it out!**

### Nothing

- Open in stegsolve 
- Click arrows on the bottom until you get to "blue plane 0" (or "gray bits")
- Scan the QR code > [http://qrs.ly/6t7r0zl](http://qrs.ly/6t7r0zl)
- Flag: **y3t\_an0th3r\_qr\_chal3ng3**

### LeverSecB

- Open in stegsolve
- Analyze > Data Extract
- In "Bit Planes", check the box for 0 in red, green, and blue (in my program, those boxes aren't visible  so I had t so I had to tab over to those boxes and select with the spacebar)
- Flag: **ilLs3yOuWH3nWeR3BOthL3553m0ti0n4l**

### Last ditch quest

- Fun fact: `.docx` files can be unzipped! (You may have to rename the file to have the `.zip` extension):
```
unzip Last-ditch-flag-quest.zip
```
- Dig around in the file structure. In this case, the flags (plural!) can be found in `docProps/core.xml`
- Flag: **i found Nemo**
- Flag: **Yet another flag**
- Another flag can be found by opening the original document itself, in white font (you can also see it in `word/document.xml`)
- Flag: **White Font!**

### Example

- Open in stegsolve
- Click arrows at bottom until you get to "alpha plane 2"
- Flag: **U_Cant_SeEE_Moi**

### CTF Example

**I haven't solved this yet -- please contact me if you figure it out!**
