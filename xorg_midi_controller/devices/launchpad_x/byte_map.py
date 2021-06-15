class ByteMap:
    class Signals:
        @staticmethod
        def is_active(byte_signal):
            return len(byte_signal) > 1 and byte_signal[-1] > 0

        @staticmethod
        def is_note(byte_signal):
            return len(byte_signal) == 3 and byte_signal[0] == ByteMap.Channels.In.NOTE

        @staticmethod
        def is_control_group(byte_signal):
            return len(byte_signal) == 3 and byte_signal[0] == ByteMap.Channels.In.CONTROL_GROUP

        @staticmethod
        def is_poly_pressure(byte_signal):
            return len(byte_signal) == 2 and byte_signal[0] == ByteMap.Channels.In.POLY_PRESSURE

        @staticmethod
        def generate_fake_signal(note, channel=0, is_active=True):
            return [
                    channel,
                    int(note),
                    127 if is_active else 0
                    ]


    class Channels:
        class In:
            NOTE  = 144
            CONTROL_GROUP = 176
            POLY_PRESSURE = 208

        class Out:
            NOTE_LIGHT_ON = 144
            NOTE_LIGHT_FLASH = 145
            NOTE_LIGHT_PULSE = 146

            CONTROL_GROUP_LIGHT_ON = 176
            CONTROL_GROUP_LIGHT_FLASH = 177
            CONTROL_GROUP_LIGHT_PULSE = 178
