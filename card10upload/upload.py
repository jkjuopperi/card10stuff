import serial
import time
from typing import Optional
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


class Card10Upload:

    def __init__(self, args):
        self._args = args
        self._serial: Optional[serial.Serial] = None
        self.log = logging.getLogger()

    def run(self):
        """
        Opens serial port, triggers the python prompt to enter paste mode,
        sends given file to the prompt and finally keeps reading debug output.
        Cancel with CTRL-C.
        """
        self._serial = serial.Serial(port=self._args.p, baudrate=115200)
        self.break_prompt()
        self.wait_prompt()
        self._serial.flushInput()
        self._serial.flushOutput()
        self.run_code()
        self.read_output()

    def break_prompt(self):
        """
        Sends a CTRL-C to break out of running program, then CTRL-E to cause
        micropython to enter paste mode.
        :return:
        """
        self.log.info("Writing CTRL-C")
        self._serial.write("\x03".encode())
        self._serial.readline()
        self.log.info("Writing CTRL-E")
        self._serial.write("\x05".encode())
        self._serial.readline()
        self._serial.write("\n".encode())

    def wait_prompt(self):
        """
        Wait for === python paste prompt.
        """
        for line in self._serial:
            self.log.debug("reading: %s", line)
            if line == b'=== \n':
                print("found python prompt in paste mode")
                break

    def run_code(self):
        with open(self._args.f) as f:
            for line in f:
                line = line.rstrip("\r\n")
                data = (line + "\r").encode()
                self.log.debug("Writing: %s", data)
                self._serial.write(data)
                time.sleep(0.01)
                self._serial.flushOutput()
                self._serial.flushInput()
            self.log.debug("Writing: %s", "\x04".encode())
            self._serial.write("\x04".encode())

    def read_output(self):
        print("Reading program output, enter CTRL-C to cancel.")
        while True:
            for line in self._serial:
                line = line.decode().rstrip("\r\n")
                print(line)


def main():
    setup_logging(logging.DEBUG)
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

    upload = Card10Upload(args)
    upload.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted")
