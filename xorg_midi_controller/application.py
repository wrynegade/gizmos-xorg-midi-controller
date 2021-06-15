from time import sleep
from contextlib import ExitStack

from xorg_midi_controller.devices import LaunchpadX

APPLICATION_REFRESH_TIME = 0.1

DEVICE_LIST = [ LaunchpadX ]

if __name__ == '__main__':
    with ExitStack() as stack:
        devices = [ stack.enter_context(D()) for D in DEVICE_LIST ]
        try:
            while True:
                for device in devices:
                    device.update(APPLICATION_REFRESH_TIME)
                sleep(APPLICATION_REFRESH_TIME)
        except KeyboardInterrupt:
            pass
