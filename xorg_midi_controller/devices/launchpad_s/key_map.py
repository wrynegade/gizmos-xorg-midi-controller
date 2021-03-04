from xorg_midi_controller.devices.binding import create_action_binding

from xorg_midi_controller.devices.launchpad_s.byte_map import ByteMap
C = ByteMap.Values.Colors


def set_key_map(Device):
    XORG = Device.XORG
    XKEYS = XORG.Keys
    PA = Device.PULSE_AUDIO

    action_callback = Device.color_button

    def bind(action, ignore_keyup=False, ignore_callback=False, **kwargs):
        return create_action_binding(
                action = action,
                action_condition = lambda b: not ignore_keyup or XORG.is_keydown(b),
                callback = None if ignore_callback else action_callback,
                **kwargs,
                )

    def bind_volume_slider(level, pulse_device_index):
        return bind(
                Device.level_volume_control,
                level=level,
                pulse_device_index=pulse_device_index,
                ignore_keyup=True,
                ignore_callback=True,
                )

    Device.KEY_BINDINGS = {
            # --- tenkeypad binding -----------------------------------------
            #'4'   : bind(XORG.bind_key, key_name='0'),
            #'5'   : bind(XORG.bind_key, key_name='1'),
            #'6'   : bind(XORG.bind_key, key_name='4'),
            #'7'   : bind(XORG.bind_key, key_name='7'),
            #'8'   : bind(XORG.bind_key, key_name='equal'),
            #'20'  : bind(XORG.bind_key, key_name='0'),
            #'21'  : bind(XORG.bind_key, key_name='2'),
            #'22'  : bind(XORG.bind_key, key_name='5'),
            #'23'  : bind(XORG.bind_key, key_name='8'),
            #'24'  : bind(XORG.bind_key, key_name='slash'),
            #'36'  : bind(XORG.bind_key, key_name='period'),
            #'37'  : bind(XORG.bind_key, key_name='3'),
            #'38'  : bind(XORG.bind_key, key_name='6'),
            #'39'  : bind(XORG.bind_key, key_name='9'),
            #'40'  : bind(XORG.bind_key, key_name='asterisk'),
            #'52'  : bind(XORG.bind_key, key_name='Return'),
            #'53'  : bind(XORG.bind_key, key_name='Return'),
            #'54'  : bind(XORG.bind_key, key_name='plus'),
            #'55'  : bind(XORG.bind_key, key_name='plus'),
            #'56'  : bind(XORG.bind_key, key_name='minus'),
            # --- default source volume slider ------------------------------
            '80'  : bind_volume_slider(level=0, pulse_device_index=1),
            '64'  : bind_volume_slider(level=0, pulse_device_index=1),
            '81'  : bind_volume_slider(level=1, pulse_device_index=1),
            '65'  : bind_volume_slider(level=1, pulse_device_index=1),
            '82'  : bind_volume_slider(level=2, pulse_device_index=1),
            '66'  : bind_volume_slider(level=2, pulse_device_index=1),
            '83'  : bind_volume_slider(level=3, pulse_device_index=1),
            '67'  : bind_volume_slider(level=3, pulse_device_index=1),
            '84'  : bind_volume_slider(level=4, pulse_device_index=1),
            '68'  : bind_volume_slider(level=4, pulse_device_index=1),
            '85'  : bind_volume_slider(level=5, pulse_device_index=1),
            '69'  : bind_volume_slider(level=5, pulse_device_index=1),
            '86'  : bind_volume_slider(level=6, pulse_device_index=1),
            '70'  : bind_volume_slider(level=6, pulse_device_index=1),
            '87'  : bind_volume_slider(level=7, pulse_device_index=1),
            '71'  : bind_volume_slider(level=7, pulse_device_index=1),
            '88'  : bind_volume_slider(level=8, pulse_device_index=1),
            '72'  : bind(PA.toggle_mute, pulse_device_index=1),
            # --- default sink volume slider --------------------------------
            '96'  : bind_volume_slider(level=0, pulse_device_index=0),
            '112' : bind_volume_slider(level=0, pulse_device_index=0),
            '97'  : bind_volume_slider(level=1, pulse_device_index=0),
            '113' : bind_volume_slider(level=1, pulse_device_index=0),
            '98'  : bind_volume_slider(level=2, pulse_device_index=0),
            '114' : bind_volume_slider(level=2, pulse_device_index=0),
            '99'  : bind_volume_slider(level=3, pulse_device_index=0),
            '115' : bind_volume_slider(level=3, pulse_device_index=0),
            '100' : bind_volume_slider(level=4, pulse_device_index=0),
            '116' : bind_volume_slider(level=4, pulse_device_index=0),
            '101' : bind_volume_slider(level=5, pulse_device_index=0),
            '117' : bind_volume_slider(level=5, pulse_device_index=0),
            '102' : bind_volume_slider(level=6, pulse_device_index=0),
            '118' : bind_volume_slider(level=6, pulse_device_index=0),
            '103' : bind_volume_slider(level=7, pulse_device_index=0),
            '119' : bind_volume_slider(level=7, pulse_device_index=0),
            '104' : bind_volume_slider(level=8, pulse_device_index=0),
            '120' : bind(PA.toggle_mute, pulse_device_index=0),
            }

    Device.AUTOMAP_BINDINGS = {
            'default' : action_callback,
            '104' : bind(XORG.bind_key, key_name=XKEYS.NUM_LOCK, ignore_callback=True),
            '105' : bind(XORG.bind_key, key_name=XKEYS.CAPS_LOCK, ignore_callback=True),
            #'106' :,
            '107' : bind(XORG.bind_key, key_name=XKEYS.MEDIA_PREV),
            '108' : bind(XORG.bind_key, key_name=XKEYS.MEDIA_PLAY),
            '109' : bind(XORG.bind_key, key_name=XKEYS.MEDIA_NEXT),
            #'110' :,
            '111' : bind(lambda _b: PA.restart(), ignore_keyup=True),
            }

    Device.FLASH_MAP = {
            '72': True,
            }

    Device.COLOR_MAP = {
        #'default': [C.BRIGHT_RED, C.DIM_RED],
        'default': [C.BRIGHT_GREEN, C.DIM_GREEN],

        #'4' : [C.BRIGHT_ORANGE, C.MEDIUM_GREEN],
        #'20': [C.BRIGHT_ORANGE, C.MEDIUM_GREEN],
        #'52': [C.BRIGHT_ORANGE, C.MEDIUM_GREEN],
        #'53': [C.BRIGHT_ORANGE, C.MEDIUM_GREEN],

        #'54': [C.BRIGHT_ORANGE, C.YELLOW_GREEN],
        #'55': [C.BRIGHT_ORANGE, C.YELLOW_GREEN],
        #'36': [C.BRIGHT_ORANGE, C.YELLOW_GREEN],

        #'5' : [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'6' : [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'7' : [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'8' : [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'21': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'22': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'23': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'24': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'37': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'38': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'39': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'40': [C.BRIGHT_ORANGE, C.MEDIUM_RED],
        #'56': [C.BRIGHT_ORANGE, C.MEDIUM_RED],

        'automap' : {
            'default': [C.YELLOW_GREEN, C.DIM_GREEN],

            '104': [C.BRIGHT_GREEN, C.MEDIUM_YELLOW],
            '105': [C.BRIGHT_AMBER, C.MEDIUM_YELLOW],

            '107': [C.BRIGHT_ORANGE, C.MEDIUM_AMBER],
            '108': [C.BRIGHT_ORANGE, C.MEDIUM_YELLOW],
            '109': [C.BRIGHT_ORANGE, C.MEDIUM_AMBER],

            '111': [C.BRIGHT_RED, C.MEDIUM_ORANGE],
            },

        'source' : {
            'no-volume': C.BRIGHT_AMBER,
            'toggle': [C.BRIGHT_RED, C.DIM_AMBER],
            'levels': [
                C.MEDIUM_RED, C.MEDIUM_RED,
                C.MEDIUM_AMBER, C.MEDIUM_AMBER, C.MEDIUM_AMBER,
                C.BRIGHT_AMBER, C.BRIGHT_AMBER,
                C.BRIGHT_YELLOW, C.BRIGHT_YELLOW,
                ],
            },

        'sink' : {
            'no-volume': C.BRIGHT_RED,
            'toggle': [C.BRIGHT_GREEN, C.DIM_GREEN],
            'levels': [
                C.BRIGHT_GREEN, C.BRIGHT_GREEN, C.BRIGHT_GREEN,
                C.YELLOW_GREEN, C.YELLOW_GREEN,
                C.BRIGHT_YELLOW,
                C.BRIGHT_RED, C.BRIGHT_RED, C.BRIGHT_RED,
                ],
            },
        }
