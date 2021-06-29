from xorg_midi_controller.devices.binding import create_action_binding

from xorg_midi_controller.devices.launchpad_x.colors import Colors as C

class MappedKeys:
    SOURCE_MUTE = 95
    PUSH_TO_TALK = 96
    SOURCE_VOLUME_COLUMNS = (6, 5)

    SINK_MUTE = 98
    SINK_CHOKE = 97
    SINK_VOLUME_COLUMNS = (7, 8)

    NUM_LOCK = 89
    CAPS_LOCK = 99

    MEDIA_NEXT = 94
    MEDIA_PREV = 93
    MEDIA_PLAY = 92

    PA_RESTART = 91

    ARROW_UP = 33
    ARROW_LEFT = 22
    ARROW_DOWN = 23
    ARROW_RIGHT = 24

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

    def bind_toggle_mute(pulse_device_index):
        signal_handler = lambda _b, pulse_device_index: PA.toggle_mute(pulse_device_index=pulse_device_index)
        return bind(
                action=signal_handler,
                pulse_device_index=pulse_device_index,
                ignore_keyup=True,
                ignore_callback=True,
                )

    Device.KEY_BINDINGS = {
            #'91' : ,
            '81' : bind(XORG.bind_key, key_name='w', ignore_keyup=True),
            '71' : bind(XORG.bind_mouse, mouse_key='1'),
            '61' : bind(Device.fast_click),
            '51' : bind(Device.fast_click, mouse_key='3'),
            #'41' : ,
            #'31' : ,
            #'21' : ,
            '11' : bind(Device.fast_key, key_name='e'),

            #'92' : ,
            #'82' : ,
            '72' : bind(XORG.bind_mouse, mouse_key='3'),
            '62' : bind(Device.fast_click),
            '52' : bind(Device.fast_click, mouse_key='3'),
            #'42' : ,
            #'32' : ,
            #'22' : ,
            '12' : bind(Device.fast_key, key_name='e'),

            #'93' : ,
            '83' : bind(XORG.bind_mouse, ignore_keyup=True),
            '73' : bind(Device.fast_click),
            '63' : bind(Device.fast_click),
            '53' : bind(Device.fast_click),
            #'43' : ,
            #'33' : ,
            #'23' : ,
            '13' : bind(Device.fast_key, key_name='e'),

            #'94' : ,
            '84' : bind(XORG.bind_mouse, ignore_keyup=True, mouse_key='3'),
            '74' : bind(Device.fast_click, mouse_key='3'),
            '64' : bind(Device.fast_click, mouse_key='3'),
            '54' : bind(Device.fast_click, mouse_key='3'),
            #'44' : ,
            #'34' : ,
            #'24' : ,
            '14' : bind(Device.fast_key, key_name='e'),

            #'95' : ,
            #'85' : ,
            #'75' : ,
            #'65' : ,
            #'55' : ,
            #'45' : ,
            #'35' : ,
            #'25' : ,
            #'15' : ,

            #'96' : ,
            #'86' : ,
            #'76' : ,
            #'66' : ,
            #'56' : ,
            #'46' : ,
            #'36' : ,
            #'26' : ,
            #'16' : ,

            #'97' : ,
            #'87' : ,
            #'77' : ,
            #'67' : ,
            #'57' : ,
            #'47' : ,
            #'37' : ,
            #'27' : ,
            #'17' : ,

            #'98' : ,
            #'88' : ,
            #'78' : ,
            #'68' : ,
            #'58' : ,
            #'48' : ,
            #'38' : ,
            #'28' : ,
            #'18' : ,

            #'99' : ### logo - LED only ###############################
            #'89' : ,
            #'79' : ,
            #'69' : ,
            #'59' : ,
            #'49' : ,
            #'39' : ,
            #'29' : ,
            '19' : bind(Device.update_all_lights, ignore_keyup=True),
            }

    Device.FLASH_MAP = {
            '95' : (True, False),
            }

    Device.PULSE_MAP = {
            }

    Device.COLOR_MAP = {
            'default': (C.SEA_GREEN, C.BLACK),

            '81' : (C.BUBBLEGUM, C.DARK_SKY),
            '83' : (C.BUBBLEGUM, C.DARK_SKY),
            '84' : (C.BUBBLEGUM, C.DARK_SKY),

            '71' : (C.RED_PURPLE, C.DARK_MAGENTA),
            '72' : (C.RED_PURPLE, C.DARK_MAGENTA),
            '61' : (C.LIGHT_MINT, C.DARK_MINT),
            '62' : (C.LIGHT_MINT, C.DARK_MINT),
            '63' : (C.LIGHT_MINT, C.DARK_MINT),
            '73' : (C.LIGHT_MINT, C.DARK_MINT),
            '53' : (C.LIGHT_MINT, C.DARK_MINT),
            '51' : (C.LIGHT_PURPLE, C.DARK_PURPLE),
            '52' : (C.LIGHT_PURPLE, C.DARK_PURPLE),
            '64' : (C.LIGHT_PURPLE, C.DARK_PURPLE),
            '74' : (C.LIGHT_PURPLE, C.DARK_PURPLE),
            '54' : (C.LIGHT_PURPLE, C.DARK_PURPLE),

            '11' : (C.GRAY_A, C.BLACK),
            '12' : (C.GRAY_A, C.BLACK),
            '13' : (C.GRAY_A, C.BLACK),
            '14' : (C.GRAY_A, C.BLACK),

            'caps_lock' : (C.RED_ORANGE_A, C.RED_PURPLE),
            'num_lock'  : (C.RED_PURPLE, C.DARK_PURPLE),

            'source' : {
                'no-volume': C.LIGHT_PINK,
                'toggle': (C.RED_A, C.BROWN_ORANGE),
                'levels': [
                    C.WHITE_ICE,
                    C.OCEAN,
                    C.BLUE_A,
                    C.VIOLET,
                    C.PURPLE_A,
                    C.RED_PURPLE,
                    C.PINK_B,
                    C.DARK_PINK,
                    ],
                },

            'sink' : {
                'no-volume': C.RED_A,
                'toggle': (C.PURPLE, C.DARK_PURPLE),
                'levels': [
                    C.RAW_TUNA,
                    C.MINT_A,
                    C.GREEN_A,
                    C.GREEN_B,
                    C.LEMON_LIME,
                    C.ELECTRIC_LEMON,
                    C.ORANGE_B,
                    C.DARK_RED,
                    ],
                },
            }


    for key, binding, color in [
            ( str(MappedKeys.SOURCE_MUTE),
                bind_toggle_mute(pulse_device_index=1),
                None,
                ),
            ( str(MappedKeys.PUSH_TO_TALK),
                bind(Device.push_to_talk),
                (C.RED_A, C.TEAL_A),
                ),
            ( str(MappedKeys.SINK_CHOKE),
                bind(Device.choke_default_sink),
                (C.LIGHT_GREEN, C.DARK_PINK),
                ),
            ( str(MappedKeys.SINK_MUTE),
                bind_toggle_mute(pulse_device_index=0),
                None,
                ),
            ( str(MappedKeys.NUM_LOCK),
                bind(XORG.bind_key, key_name=XKEYS.NUM_LOCK, ignore_callback=True),
                None,
                ),
            ( str(MappedKeys.CAPS_LOCK),
                bind(XORG.bind_key, key_name=XKEYS.CAPS_LOCK, ignore_callback=True),
                None,
                ),
            ( str(MappedKeys.MEDIA_NEXT),
                bind(XORG.bind_key, key_name=XKEYS.MEDIA_NEXT),
                (C.MINT_A, C.DARK_MINT),
                ),
            ( str(MappedKeys.MEDIA_PREV),
                bind(XORG.bind_key, key_name=XKEYS.MEDIA_PREV),
                (C.MINT_A, C.DARK_MINT),
                ),
            ( str(MappedKeys.MEDIA_PLAY),
                bind(XORG.bind_key, key_name=XKEYS.MEDIA_PLAY),
                (C.TEAL_A, C.DARK_TEAL),
                ),
            ( str(MappedKeys.PA_RESTART),
                bind(lambda _b: PA.restart(), ignore_keyup=True),
                (C.LIGHT_MAGENTA, C.DARK_PEACH),
                ),
            ( str(MappedKeys.ARROW_UP),
                bind(XORG.bind_key, key_name=XKEYS.ARROW_UP),
                (C.BLUE_A, C.BLACK),
                ),
            ( str(MappedKeys.ARROW_DOWN),
                bind(XORG.bind_key, key_name=XKEYS.ARROW_DOWN),
                (C.BLUE_A, C.BLACK),
                ),
            ( str(MappedKeys.ARROW_LEFT),
                bind(XORG.bind_key, key_name=XKEYS.ARROW_LEFT),
                (C.BLUE_A, C.BLACK),
                ),
            ( str(MappedKeys.ARROW_RIGHT),
                bind(XORG.bind_key, key_name=XKEYS.ARROW_RIGHT),
                (C.BLUE_A, C.BLACK),
                ),
            ]:
        Device.KEY_BINDINGS[key] = binding
        if color is not None:
            Device.COLOR_MAP[key] = color

    for columns, pulse_device_index in [
            (MappedKeys.SINK_VOLUME_COLUMNS, 0),
            (MappedKeys.SOURCE_VOLUME_COLUMNS, 1),
            ]:
        for column in columns:
            for x in range(Device.LEVELS):
                Device.KEY_BINDINGS[str(10*(x+1) + column)]\
                        = bind( action = Device.level_volume_control,
                                level = x,
                                pulse_device_index = pulse_device_index,
                                ignore_keyup = True,
                                ignore_callback = True,
                                )
