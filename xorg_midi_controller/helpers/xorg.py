from os import popen
from subprocess import call


class XorgHelper:
    # pylint: disable=no-self-use

    class Keys:
        NUM_LOCK = 'Num_Lock'
        NUM_LOCK_REGEX = 'Num Lock'

        CAPS_LOCK = 'Caps_Lock'
        CAPS_LOCK_REGEX = 'Caps Lock'

        MEDIA_PLAY = 'XF86AudioPlay'
        MEDIA_NEXT = 'XF86AudioNext'
        MEDIA_PREV = 'XF86AudioPrev'

        ARROW_LEFT  = 'Left'
        ARROW_DOWN  = 'Down'
        ARROW_UP    = 'Up'
        ARROW_RIGHT = 'Right'

    def is_keydown(self, byte_signal):
        return len(byte_signal) == 3 and byte_signal[2] > 0

    def bind_key(self, byte_signal, key_name, callback=None):
        call([
            'xdotool',
            'keydown' if self.is_keydown(byte_signal) else 'keyup',
            key_name,
            ])
        if callback is not None:
            callback(byte_signal)

    def bind_mouse(self, byte_signal, callback=None, mouse_key='1'):
        call([
            'xdotool',
            'mousedown' if self.is_keydown(byte_signal) else 'mouseup',
            mouse_key,
            ])
        if callback is not None:
            callback(byte_signal)

    def key(self, key_name):
        call(['xdotool', 'key', key_name])

    def keydown(self, key_name):
        call(['xdotool', 'keydown', key_name])

    def keyup(self, key_name):
        call(['xdotool', 'keyup', key_name])

    def mousedown(self, mouse_key):
        call(['xdotool', 'mousedown', mouse_key])

    def mouseup(self, mouse_key):
        call(['xdotool', 'mouseup', mouse_key])

    def key_status(self, key_regex):
        cmd = f'xset q | grep -q "{key_regex}:\\s*on" && echo 1'
        return bool(popen(cmd).read())
