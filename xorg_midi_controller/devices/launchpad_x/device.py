from math import ceil

from xorg_midi_controller.devices.device import Device

import xorg_midi_controller.devices.launchpad_x.animation as ANIMATION
from xorg_midi_controller.devices.launchpad_x.byte_map import ByteMap
from xorg_midi_controller.devices.launchpad_x.key_map import set_key_map, MappedKeys


class LaunchpadX(Device):

    LEVELS = 8

    COLOR_MAP = {}
    FLASH_MAP = {}
    PULSE_MAP = {}

    MIDI_CLOCK = 30


    def __init__(self, max_output=133, max_input=182):
        super().__init__(name='Launchpad X', regex=r'^.*Launchpad X LPX MIDI.*$')
        self.MAX_OUTPUT_VOLUME = max_output
        self.MAX_INPUT_VOLUME = max_input

        set_key_map(self)

        self.UPDATE_LIST.append(self.update_animation)


    def __exit__(self, *args, **kwargs):
        ANIMATION.reset_all_lights(self)
        super().__exit__(*args, **kwargs)

    def activate(self):
        super().activate()
        ANIMATION.boot(self)

    def animation_callback(self, byte_signal):
        ANIMATION.color_button(self, byte_signal)
        super().animation_callback(byte_signal)

    def input_callback(self, midi_signal_in, *args, **kwargs):
        byte_signal = midi_signal_in[0]

        if ByteMap.Signals.is_poly_pressure(byte_signal):
            pass
        else:
            super().input_callback(midi_signal_in, *args, **kwargs)


    # --- update functions ----------------------------------------------------------------

    color_button = ANIMATION.color_button
    update_volume_bar = ANIMATION.update_volume_bar
    update_button_visual = ANIMATION.update_button_visual
    update_all_lights = ANIMATION.update_all_lights

    def update_animation(self, _elapsed_time):
        for volume_bar in [
                { 'columns'    : MappedKeys.SOURCE_VOLUME_COLUMNS,
                    'percentage' : float(self.PULSE_AUDIO.get_default_source_volume()),
                    'color_map'  : self.COLOR_MAP['source'],
                    'max_volume' : self.MAX_INPUT_VOLUME,
                    },
                { 'columns'    : MappedKeys.SINK_VOLUME_COLUMNS,
                    'percentage' : float(self.PULSE_AUDIO.get_default_sink_volume()),
                    'color_map'  : self.COLOR_MAP['sink'],
                    'max_volume' : self.MAX_OUTPUT_VOLUME,
                    },
                ]:
            self.update_volume_bar(**volume_bar)

        for key_visual in [
                { 'note': MappedKeys.NUM_LOCK,
                    'is_active': self.XORG.key_status(key_regex=self.XORG.Keys.NUM_LOCK_REGEX),
                    'color_map': self.COLOR_MAP['num_lock'],
                    },
                { 'note': MappedKeys.CAPS_LOCK,
                    'is_active': self.XORG.key_status(key_regex=self.XORG.Keys.CAPS_LOCK_REGEX),
                    'color_map': self.COLOR_MAP['caps_lock'],
                    },
                { 'note': MappedKeys.SOURCE_MUTE,
                    'is_active': not self.PULSE_AUDIO.get_default_source_mute(),
                    'color_map': self.COLOR_MAP['source']['toggle'],
                    },
                { 'note': MappedKeys.SINK_MUTE,
                    'is_active': not self.PULSE_AUDIO.get_default_sink_mute(),
                    'color_map': self.COLOR_MAP['sink']['toggle'],
                    },
                ]:
            self.update_button_visual(**key_visual)

    # --- actions -------------------------------------------------------------------------

    def get_channel(self, note, is_active, force=None):
        is_control_group = int(note) % 10 == 9

        is_flashing = self.FLASH_MAP.get(str(note), [False, False])[0 if is_active else 1]
        is_pulsing = self.PULSE_MAP.get(str(note), [False, False])[0 if is_active else 1]

        C = ByteMap.Channels.Out

        if force == 'solid':
            channel = C.CONTROL_GROUP_LIGHT_PULSE if is_control_group else C.NOTE_LIGHT_PULSE
        elif force == 'pulse':
            channel = C.CONTROL_GROUP_LIGHT_PULSE if is_control_group else C.NOTE_LIGHT_PULSE
        elif force == 'flash':
            channel = C.CONTROL_GROUP_LIGHT_PULSE if is_control_group else C.NOTE_LIGHT_PULSE

        elif is_control_group:
            if is_pulsing:
                channel = C.CONTROL_GROUP_LIGHT_PULSE
            elif is_flashing:
                channel = C.CONTROL_GROUP_LIGHT_FLASH
            else:
                channel = C.CONTROL_GROUP_LIGHT_ON
        else:
            if is_pulsing:
                channel = C.NOTE_LIGHT_PULSE
            if is_flashing:
                channel = C.NOTE_LIGHT_FLASH
            else:
                channel = C.NOTE_LIGHT_ON

        return channel

    def level_volume_control(self, _byte_signal, level, pulse_device_index=0):
        max_volume = self.MAX_INPUT_VOLUME if pulse_device_index == 1 else self.MAX_OUTPUT_VOLUME
        self.PULSE_AUDIO.volume_control(
                volume_percentage = ceil(max_volume * level / self.LEVELS),
                pulse_device_index = pulse_device_index,
                )

    def choke_default_sink(self, byte_signal):
        self.PULSE_AUDIO.set_mute(
                pulse_device_index=0,
                mute=self.XORG.is_keydown(byte_signal),
                )

    def push_to_talk(self, byte_signal):
        self.PULSE_AUDIO.set_mute(
                pulse_device_index=1,
                mute=not self.XORG.is_keydown(byte_signal),
                )

    def fast_click(self, _byte_signal=None, mouse_key='1'):
        self.XORG.mousedown(mouse_key=mouse_key)
        self.XORG.mouseup(mouse_key=mouse_key)

    def fast_key(self, _byte_signal=None, key_name='a'):
        self.XORG.keydown(key_name=key_name)
        self.XORG.keyup(key_name=key_name)
