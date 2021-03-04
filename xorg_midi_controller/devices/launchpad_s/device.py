from math import floor

from xorg_midi_controller.devices.device import Device

import xorg_midi_controller.devices.launchpad_s.animation as ANIMATION
from xorg_midi_controller.devices.launchpad_s.byte_map import ByteMap
from xorg_midi_controller.devices.launchpad_s.key_map import set_key_map


class LaunchpadS(Device):
    COLS = 9
    ROWS = 8

    FLASH_CYCLE_TIME = 0.5
    FLASH_CYCLE_ACTIVE = True

    FLASH_MAP = None
    COLOR_MAP = None

    MAX_OUTPUT_LEVEL = COLS - 1
    MAX_INPUT_LEVEL  = COLS - 1

    AUTOMAP_BINDINGS = {}

    color_button = ANIMATION.color_button

    def __init__(self, max_output=150, max_input=150):
        super().__init__(name='Launchpad S', regex=r'^.*Launchpad S.*$')
        self.CURRENT_ELASPED_FLASH_CYCLE = self.FLASH_CYCLE_TIME
        self.MAX_OUTPUT_VOLUME = max_output
        self.MAX_INPUT_VOLUME  = max_input
        set_key_map(self)

        self.UPDATE_LIST.append(self.update_flash_cycle)
        self.UPDATE_LIST.append(self.update_animation)

    def __exit__(self, *args, **kwargs):
        self.send_signal(*ByteMap.Signals.RESET_ALL_LIGHTS)
        super().__exit__(*args, **kwargs)

    def activate(self):
        super().activate()
        ANIMATION.boot(self)

    def input_callback(self, midi_signal_in, *args, **kwargs):
        byte_signal = midi_signal_in[0]
        key = str(byte_signal[1])

        if ByteMap.Signals.is_automap_signal(byte_signal):
            if key not in self.AUTOMAP_BINDINGS.keys():
                key = 'default'
            self.AUTOMAP_BINDINGS[key](byte_signal)
        else:
            super().input_callback(midi_signal_in, *args, **kwargs)

    def animation_callback(self, byte_signal):
        ANIMATION.color_button(self, byte_signal)
        super().animation_callback(byte_signal)


    # --- update functions ----------------------------------------------------------------

    def update_flash_cycle(self, elapsed_time):
        self.CURRENT_ELASPED_FLASH_CYCLE -= elapsed_time

        if self.CURRENT_ELASPED_FLASH_CYCLE < 0:
            self.FLASH_CYCLE_ACTIVE = not self.FLASH_CYCLE_ACTIVE
            self.CURRENT_ELASPED_FLASH_CYCLE = self.FLASH_CYCLE_TIME

    def update_animation(self, _elapsed_time):
        ANIMATION.update_source_volume_visual(self)
        ANIMATION.update_source_mute_visual(self)
        ANIMATION.update_sink_volume_visual(self)
        ANIMATION.update_sink_mute_visual(self)
        ANIMATION.update_num_lock_visual(self)
        ANIMATION.update_caps_lock_visual(self)


    # --- actions -------------------------------------------------------------------------

    def level_volume_control(self, _byte_signal, level, pulse_device_index=0):
        self.PULSE_AUDIO.volume_control(
                volume_percentage = floor(self.MAX_INPUT_VOLUME * level / self.MAX_INPUT_LEVEL),
                pulse_device_index = pulse_device_index,
                )
