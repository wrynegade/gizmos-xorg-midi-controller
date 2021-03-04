
from xorg_midi_controller.devices.device import Device
from xorg_midi_controller.devices.komplete_audio_6.maschine_mk_2.key_map import set_key_map


class MaschineMK2(Device):
    TARGET_PULSE_AUDIO_INDEX = 0

    def __init__(self):
        super().__init__(name='Maschine MK 2', regex=r'^.*Komplete.*$')
        set_key_map(self)

    def input_callback(self, midi_signal_in, *args, **kwargs):
        byte_signal = midi_signal_in[0]

        is_clock_reset = len(byte_signal) == 1 and byte_signal[0] == 255

        if is_clock_reset or len(byte_signal) < 2:
            return

        if byte_signal[0] == 176 and byte_signal[1] == 1:
            self.KEY_BINDINGS['control_wheel'](byte_signal)

        else:
            super().input_callback(midi_signal_in, *args, **kwargs)

    # --- actions -------------------------------------------------------------------------

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

    def relative_volume_control(self, byte_signal):
        self.PULSE_AUDIO.relative_volume_control(byte_signal, self.TARGET_PULSE_AUDIO_INDEX)

    def set_target_audio_index(self, byte_signal, index):
        if self.XORG.is_keydown(byte_signal):
            self.TARGET_PULSE_AUDIO_INDEX = index
        else:
            self.TARGET_PULSE_AUDIO_INDEX = 0

    def toggle_mute(self, *_args, **_kwargs):
        self.PULSE_AUDIO.toggle_mute(self.TARGET_PULSE_AUDIO_INDEX)
