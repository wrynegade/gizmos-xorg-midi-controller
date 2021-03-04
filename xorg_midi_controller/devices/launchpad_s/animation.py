from math import floor
from time import time, sleep

from xorg_midi_controller.helpers.general import fix_value_to_bounds
from xorg_midi_controller.devices.launchpad_s.byte_map import ByteMap


def color_button(launchpad_s, byte_signal=None, color_map=None, force_default=False):
    is_automap_key = ByteMap.Signals.is_automap_signal(byte_signal)

    note_key = byte_signal[1]
    note = str(note_key)

    if color_map is None:
        color_key = 'default' if force_default else note
        color_map = launchpad_s.COLOR_MAP['automap'] if is_automap_key else launchpad_s.COLOR_MAP

        active_color, inactive_color = color_map.get(color_key, color_map['default'])
    else:
        active_color, inactive_color = color_map

    is_active = launchpad_s.XORG.is_keydown(byte_signal)

    is_light_on = any([
            not launchpad_s.FLASH_MAP.get(note, False), # non-flashing lights are always on
            not is_active, # non-active lights are always on (uses inactive color)
            launchpad_s.FLASH_CYCLE_ACTIVE, # flashing lights are on when the flash cycle is active
            ])

    if is_light_on:
        if is_automap_key:
            channel = ByteMap.Channels.Out.AUTOMAP_LIGHT_ON
        else:
            channel = ByteMap.Channels.Out.BUTTON_LIGHT_ON
    else:
        channel = ByteMap.Channels.Out.LIGHT_OFF

    launchpad_s.send_signal(
            channel = channel,
            key     = note_key,
            payload = active_color if is_active else inactive_color,
            )

def boot(launchpad_s):
    sleep_time = 0.03
    multiplier = .98
    pause_time = 0.5

    channels = ByteMap.Channels.Out

    automap_signal = lambda x: [channels.AUTOMAP_LIGHT_ON, 104 + x, 0]
    button_signal = lambda x: [channels.BUTTON_LIGHT_ON, floor(x/launchpad_s.COLS)*16 + x%launchpad_s.COLS, 0]

    for x in range(launchpad_s.COLS - 1):
        launchpad_s.color_button(
                byte_signal    = automap_signal(x),
                force_default  = True,
                )
        sleep(sleep_time)
        sleep_time *= multiplier

    for x in range(launchpad_s.ROWS * launchpad_s.COLS):
        launchpad_s.color_button(
                byte_signal    = button_signal(x),
                force_default  = True,
                )
        sleep(sleep_time)
        sleep_time *= multiplier

    start = time()
    current_status_signals = []
    for x in range(launchpad_s.COLS - 1):
        current_status_signals.append(automap_signal(x))
    for x in range(launchpad_s.ROWS*launchpad_s.COLS):
        current_status_signals.append(button_signal(x))

    sleep(min(pause_time - (start - time()), 0))
    for signal in current_status_signals:
        launchpad_s.color_button(signal)


def update_num_lock_visual(launchpad_s):
    launchpad_s.color_button(
            byte_signal = ByteMap.Signals.generate_fake_midi_signal(
                is_automap=True,
                note=104,
                on=launchpad_s.XORG.key_status(launchpad_s.XORG.Keys.NUM_LOCK_REGEX),
                )
            )

def update_caps_lock_visual(launchpad_s):
    launchpad_s.color_button(
            byte_signal = ByteMap.Signals.generate_fake_midi_signal(
                is_automap=True,
                note=105,
                on=launchpad_s.XORG.key_status(launchpad_s.XORG.Keys.CAPS_LOCK_REGEX),
                )
            )

def update_source_mute_visual(launchpad_s):
    is_muted = launchpad_s.PULSE_AUDIO.get_default_source_mute()
    launchpad_s.color_button(
            byte_signal = ByteMap.Signals.generate_fake_midi_signal(note=72, on=not is_muted),
            color_map=launchpad_s.COLOR_MAP['source']['toggle'],
            )

def update_sink_mute_visual(launchpad_s):
    is_muted = launchpad_s.PULSE_AUDIO.get_default_sink_mute()
    launchpad_s.color_button(
            byte_signal = ByteMap.Signals.generate_fake_midi_signal(note=120, on=not is_muted),
            color_map=launchpad_s.COLOR_MAP['sink']['toggle'],
            )


def update_sink_volume_visual(launchpad_s):
    INDICES = { 'main': [96, 104], 'staggered': [112, 119] }

    percentage = float(launchpad_s.PULSE_AUDIO.get_default_sink_volume())
    color_map = launchpad_s.COLOR_MAP['sink']

    stylize_volume_bar(launchpad_s, percentage, color_map, launchpad_s.MAX_OUTPUT_LEVEL, INDICES)

def update_source_volume_visual(launchpad_s):
    INDICES = { 'main': [80, 88], 'staggered': [64, 71] }

    percentage = float(launchpad_s.PULSE_AUDIO.get_default_source_volume())
    color_map = launchpad_s.COLOR_MAP['source']

    stylize_volume_bar(launchpad_s, percentage, color_map, launchpad_s.MAX_INPUT_LEVEL, INDICES)

def stylize_volume_bar(launchpad_s, percentage, color_map, max_volume, INDICES):
    level = fix_value_to_bounds(
            floor(round(
                percentage / launchpad_s.MAX_OUTPUT_VOLUME * launchpad_s.MAX_OUTPUT_LEVEL
                )),
            0, max_volume)

    get_active_color = lambda x: [
            color_map['levels'][x] if level > 0 else color_map['no-volume'],
            None
            ]

    for x in range(level + 1):
        main_index = INDICES['main'][0] + x
        staggered_index = fix_value_to_bounds(
                INDICES['staggered'][0] + x - 1,
                INDICES['staggered'][0],
                INDICES['staggered'][1],
                )

        for note in [main_index, staggered_index]:
            launchpad_s.color_button(
                    byte_signal = ByteMap.Signals.generate_fake_midi_signal(note=note),
                    color_map = get_active_color(x),
                    )

    inactive_colors = [None, launchpad_s.COLOR_MAP['default'][1]]

    for x in range(launchpad_s.MAX_INPUT_LEVEL - level):
        main_index = INDICES['main'][1] -x
        staggered_index = fix_value_to_bounds(
                INDICES['staggered'][1] - x,
                INDICES['staggered'][0] + 1,
                INDICES['staggered'][1],
                )

        for note in [main_index, staggered_index]:
            launchpad_s.color_button(
                    byte_signal = ByteMap.Signals.generate_fake_midi_signal(note=note, on=False),
                    color_map=inactive_colors,
                    )
