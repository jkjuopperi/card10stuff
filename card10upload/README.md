# card10upload #

Tool to run code on CCCAmp card10 badge with ease,
without constantly rebooting into different modes.

Example usage on macOS
```
python3 -m venv venv
. venv/bin/activate
pip install pyserial
sudo python3 card10upload.py -f kikkeli.py \
   -p /dev/tty.usbmodem14101
```
