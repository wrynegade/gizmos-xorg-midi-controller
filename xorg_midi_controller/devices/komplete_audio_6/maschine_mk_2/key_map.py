from xorg_midi_controller.devices.binding import create_action_binding


def set_key_map(Device):
    XORG = Device.XORG
    XKEYS = XORG.Keys
    PA = Device.PULSE_AUDIO

    def bind(action, ignore_keyup=False, **kwargs):
        return create_action_binding(
                action = action,
                action_condition = lambda b: not ignore_keyup or XORG.is_keydown(b),
                callback = lambda _b: None,
                **kwargs,
                )

    Device.KEY_BINDINGS = {
            # --- custom control keys -------------------------------------
            'control_wheel': bind(Device.relative_volume_control),
            # --- velocity-sensitive pads (left-to-right bottom-to-top) ---
            #'24' :
            #'25' :
            #'26' :
            #'27' :
            #'28' :
            #'29' :
            #'30' :
            #'31' :
            '32' : bind(XORG.bind_mouse),
            '33' : bind(XORG.bind_mouse),
            '34' : bind(XORG.bind_mouse),
            '35' : bind(XORG.bind_mouse),
            '36' : bind(XORG.bind_mouse, mouse_key='3'),
            '37' : bind(XORG.bind_mouse, mouse_key='3'),
            '38' : bind(XORG.bind_mouse, mouse_key='3'),
            '39' : bind(XORG.bind_mouse, mouse_key='3'),
            # --- pads ----------------------------------------------------
            #'112': # scene
            #'113': # pattern
            #'114': # pad mode
            #'115': # navigate
            #'116': # duplicate
            #'117': # select
            #'118': # solo
            '119': bind(Device.choke_default_sink), # mute
            # --- transport -----------------------------------------------
            #'104': # restart
            '105': bind(XORG.bind_key, key_name=XKEYS.MEDIA_PREV),
            '106': bind(XORG.bind_key, key_name=XKEYS.MEDIA_NEXT),
            #'107': # grid
            '108': bind(XORG.bind_key, key_name=XKEYS.MEDIA_PLAY),
            '109': bind(Device.push_to_talk),
            #'110': # erase
            # --- groups --------------------------------------------------
            '80' : bind(Device.set_target_audio_index, index=1), # A
            #'81' : # B
            #'82' : # C
            #'83' : # D
            #'91' : # E
            #'92' : # F
            #'93' : # G
            #'94' : # H
            # --- top section ---------------------------------------------
            '85' : bind(lambda _b: PA.restart(), ignore_keyup=True),
            #'86' : # step
            #'87' : # browse
            #'88' : # sampling
            #'89' : # all
            #'90' : # auto write
            #'46' : # top row 1
            #'47' : # top row 2
            #'48' : # top row 3
            #'49' : # top row 4
            #'50' : # top row 5
            #'51' : # top row 6
            #'52' : # top row 7
            #'53' : # top row 8
            # --- master --------------------------------------------------
            #'7'  : # volume
            #'9'  : # swing
            #'3'  : # tempo
            #'98' : # <<
            #'99' : # >>
            #'100': # enter
            '102': bind(Device.toggle_mute, ignore_keyup=True),
            #'111': # note repeat
            }
