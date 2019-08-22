import serial
import time
import uuid
import argparse
import logging
import sys


def setup_logging(level: int):
    root = logging.getLogger()
    root.setLevel(level)
    formatter = logging.Formatter('%(name)s(%(levelname)s): %(message)s')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    root.addHandler(ch)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)


setup_logging(logging.DEBUG)
log = logging.getLogger()


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", type=str,
    help="Code to run (python file)",
    required=True)
parser.add_argument(
    "-p", type=str,
    help="Serial port, e.g. /dev/tty.usbmodem14101",
    required=True)

args = parser.parse_args()
id = str(uuid.uuid4()).encode()


def break_prompt():
    s.write("\x03".encode())
    time.sleep(0.1)
    s.write("\x05".encode())
    time.sleep(0.1)
    s.write("\n".encode())


def wait_prompt():
    for line in s:
        print("line=%s" % (line,))
        if line == b'=== \n':
            print("found python prompt in paste mode")
            break


def run_code():
    with open(args.f) as f:
        for line in f:
            line = line.rstrip("\r\n")
            data = (line + "\r").encode()
            log.debug("Writing: %s", data)
            s.write(data)
            time.sleep(0.01)
            s.flushOutput()
            s.flushInput()
        log.debug("Writing: %s", "\x04".encode())
        s.write("\x04".encode())


s = serial.Serial(port=args.p, baudrate=115200)

break_prompt()
wait_prompt()
s.flushInput()
s.flushOutput()
run_code()

while True:
    for line in s:
        line = line.decode().rstrip("\r\n")
        print(line)

