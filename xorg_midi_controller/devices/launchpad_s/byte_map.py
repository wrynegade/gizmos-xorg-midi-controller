class ByteMap:
    class Signals:
        RESET_ALL_LIGHTS = [0xb0, 0x00, 0x00]

        @staticmethod
        def is_active(byte_signal):
            return len(byte_signal) == 3 and byte_signal[2] == ByteMap.Values.ACTIVE

        @staticmethod
        def is_automap_signal(byte_signal):
            return byte_signal[0] == ByteMap.Channels.In.AUTOMAP

        @staticmethod
        def generate_fake_midi_signal(is_automap=False, note=0, on=True):
            c = ByteMap.Channels.Out
            return [
                    c.AUTOMAP_LIGHT_ON if is_automap else c.BUTTON_LIGHT_ON,
                    note,
                    127 if on else 0,
                    ]

    class Channels:
        class In:
            BUTTON  = 127
            AUTOMAP = 176 # top row buttons (includes 'mixer' button)

        class Out:
            AUTOMAP_LIGHT_ON = 0xb0
            BUTTON_LIGHT_ON  = 0x90
            LIGHT_OFF        = 0x80 # use for both automap and normal button

    class Values:
        INACTIVE = 0
        ACTIVE = 127

        class Colors:
            # Colors are combinations of red (R) and green (G) bits
            # 0b00GG11RR
            OFF = 0b00001100

            DIM_GREEN    = 0b00011100
            MEDIUM_GREEN = 0b00101100
            BRIGHT_GREEN = 0b00111100

            DIM_RED    = 0b00001101
            MEDIUM_RED = 0b00001110
            BRIGHT_RED = 0b00001111

            DIM_AMBER    = 0b00011101
            MEDIUM_AMBER = 0b00101110
            BRIGHT_AMBER = 0b00111111

            MEDIUM_ORANGE = 0b00011110
            BRIGHT_ORANGE = 0b00101111
            RED_ORANGE    = 0b00011111

            MEDIUM_YELLOW = 0b00101101
            BRIGHT_YELLOW = 0b00111110
            YELLOW_GREEN  = 0b00111101
