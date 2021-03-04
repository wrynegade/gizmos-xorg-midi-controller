from subprocess import call
from os import popen


class PulseAudioHelper:
    # pylint: disable=no-self-use

    def __init__(self, device_list=None):
        if device_list is None:
            device_list = [['sink', '@DEFAULT_SINK@'], ['source', '@DEFAULT_SOURCE@']]

        self.PULSE_DEVICE_LIST = device_list

    def restart(self):
        call(['pulseaudio', '-k'])

    def relative_volume_control(self, byte_signal, pulse_device_index=0):
        level = byte_signal[2]
        is_volume_up = level < (128/2)

        relative_level = level if is_volume_up else 128 - level
        relative_level *= 4

        pulse_device = self.PULSE_DEVICE_LIST[pulse_device_index]

        call([
            'pactl',
            f'set-{pulse_device[0]}-volume',
            pulse_device[1],
            f'{"+" if is_volume_up else "-"}{relative_level}%',
            ])

    def volume_control(self, volume_percentage, pulse_device_index=0):
        pulse_device = self.PULSE_DEVICE_LIST[pulse_device_index]
        call([
            'pactl',
            f'set-{pulse_device[0]}-volume',
            pulse_device[1],
            f'{volume_percentage}%',
            ])

    def get_default_sink_volume(self):
        cmd = 'amixer -D pulse sget Master | grep "Front Left:" | sed "s/^.*\\[\\(.*\\)%.*$/\\1/" || return 0'
        return popen(cmd).read()

    def get_default_sink_mute(self):
        cmd = 'amixer -D pulse get Master | grep -q off && echo 1'
        is_muted = bool(popen(cmd).read())
        return is_muted

    def get_default_source_volume(self):
        cmd = 'amixer -D pulse sget Capture | grep "Front Left:" | sed "s/^.*\\[\\(.*\\)%.*$/\\1/" || return 0'
        return popen(cmd).read()

    def get_default_source_mute(self):
        cmd = 'amixer -D pulse get Capture | grep -q off && echo 1'
        is_muted = bool(popen(cmd).read())
        return is_muted

    def set_mute(self, pulse_device_index=0, mute=False):
        pulse_device = self.PULSE_DEVICE_LIST[pulse_device_index]
        call([
            'pactl',
            f'set-{pulse_device[0]}-mute',
            pulse_device[1],
            '1' if mute else '0',
            ])

    def toggle_mute(self, pulse_device_index=0):
        pulse_device = self.PULSE_DEVICE_LIST[pulse_device_index]
        call([
            'pactl',
            f'set-{pulse_device[0]}-mute',
            pulse_device[1],
            'toggle',
            ])
