import re
from time import sleep

from rtmidi import MidiIn, MidiOut # pylint: disable=no-name-in-module

from xorg_midi_controller.helpers.pulse_audio import PulseAudioHelper
from xorg_midi_controller.helpers.xorg import XorgHelper


class Device:
    MIDI_IN = None
    MIDI_OUT = None
    MIDI_PORT_COUNT = 0
    IS_FIRST_CONNECTION = True

    UPDATE_LIST = []
    KEY_BINDINGS = {}

    PULSE_AUDIO = PulseAudioHelper()
    XORG        = XorgHelper()

    def __init__(self, name='Generic Device', regex=None):
        self.NAME = name
        self.DEVICE_REGEX = regex
        self.UPDATE_LIST.append(self.update_midi_connection_on_reconnect)

    def __enter__(self):
        self.MIDI_IN  = MidiIn()
        self.MIDI_OUT = MidiOut()
        return self

    def __exit__(self, _type, _value, _traceback):
        del self.MIDI_IN, self.MIDI_OUT

    def __repr__(self):
        return self.NAME

    def update(self, ELAPSED_TIME):
        for update in self.UPDATE_LIST:
            update(ELAPSED_TIME)

    def send_signal(self, channel, key, payload):
        self.MIDI_OUT.send_message([channel, key, payload])

    def update_midi_connection_on_reconnect(self, _elapsed_time):
        current_port_count = len([x for x in self.MIDI_OUT.get_ports() if not re.search(r'[rR]t[Mm]idi', x)])

        if current_port_count != self.MIDI_PORT_COUNT:
            self.MIDI_PORT_COUNT = current_port_count
            self.activate()

    def activate(self):
        if self.DEVICE_REGEX is not None:
            self.activate_ports()

    def activate_ports(self):
        activated = False
        self.MIDI_IN.close_port()
        self.MIDI_OUT.close_port()

        if not self.IS_FIRST_CONNECTION:
            print(f'{self} disconnected!')

        sleep(1.0)

        for midi in (self.MIDI_IN, self.MIDI_OUT):
            port_number = None
            for i, port_name in enumerate(midi.get_ports()):
                if re.search(self.DEVICE_REGEX, port_name):
                    port_number = i
                    break

            if port_number is not None:
                midi.open_port(port_number)
                activated = True

        if activated:
            self.IS_FIRST_CONNECTION = False
            print(f'{self} connected!')

        self.MIDI_IN.set_callback(self.input_callback)

    def input_callback(self, midi_signal_in, *_args, **_kwargs):
        byte_signal = midi_signal_in[0]
        key = str(byte_signal[1])

        if key in self.KEY_BINDINGS.keys():
            self.KEY_BINDINGS[key](byte_signal)
        else:
            self.animation_callback(byte_signal)

    def animation_callback(self, byte_signal):
        print(f'{self}:{byte_signal}')
