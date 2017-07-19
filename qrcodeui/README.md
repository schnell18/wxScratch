# Introduction
This is a demo program to generate and display QR code instantly.
It supports:

- clipboard integration
- L, M, Q, H error correction levels
- customizable margin and pixel size

# How to build standalone binary
Make sure you install pyinstaller 3.1.1.
Then run:

    pyinstaller -onefile -noconsole qrcodeui.py

and get the .exe file under dist directory.
