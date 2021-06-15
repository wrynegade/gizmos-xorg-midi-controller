from math import floor
from time import sleep

from xorg_midi_controller.helpers.general import fix_value_to_bounds

from xorg_midi_controller.devices.launchpad_x.byte_map import ByteMap
from xorg_midi_controller.devices.launchpad_x.key_map import MappedKeys


def color_button(launchpad_x, byte_signal=None, color_map=None, force_default=False, force=None):
    note = byte_signal[1]

    if color_map is None:
        color_key = 'default' if force_default else str(note)
        color_map = launchpad_x.COLOR_MAP

        active_color, inactive_color = color_map.get(color_key, color_map['default'])
    else:
        active_color, inactive_color = color_map

    is_active = ByteMap.Signals.is_active(byte_signal)
    color = active_color if is_active else inactive_color

    if color is not None:
        launchpad_x.send_signal(
                channel = launchpad_x.get_channel(note, is_active, force=force),
                key     = note,
                payload = active_color if is_active else inactive_color,
                )

def all_note_values():
    return [
            *range(11, 20),
            *range(21, 30),
            *range(31, 40),
            *range(41, 50),
            *range(51, 60),
            *range(61, 70),
            *range(71, 80),
            *range(81, 90),
            *range(91, 100),
            ]

def reset_all_lights(launchpad_x):
    CHANNELS = ByteMap.Channels.Out
    for x in all_note_values():
        launchpad_x.send_signal(
                channel = CHANNELS.NOTE_LIGHT_ON if x%10==9 else CHANNELS.CONTROL_GROUP_LIGHT_ON,
                key = x,
                payload = 0,
                )

def boot(launchpad_x):
    reset_all_lights(launchpad_x)

    sleep_time = 0.03
    multiplier = .98
    pause_time = 0.5

    NOTE_ON = ByteMap.Channels.Out.NOTE_LIGHT_PULSE
    CONTROL_ON = ByteMap.Channels.Out.CONTROL_GROUP_LIGHT_PULSE

    signals = [
            [ NOTE_ON if note%10==9 or note>90 else CONTROL_ON, note ]
            for note in all_note_values()
            ]

    for signal in signals:
        launchpad_x.color_button([*signal, 127], force_default=True, force='solid')
        sleep(sleep_time)
        sleep_time *= multiplier

    sleep(pause_time)
    for signal in signals:
        launchpad_x.color_button([*signal, 0])


def update_button_visual(launchpad_x, note, is_active, color_map=None):
    launchpad_x.color_button(
            byte_signal = ByteMap.Signals.generate_fake_signal(note=note, is_active=is_active),
            color_map = color_map,
            )

def update_volume_bar(launchpad_x, percentage, color_map, max_volume, columns):
    MAX_LEVEL = launchpad_x.LEVELS - 1
    LEVEL = fix_value_to_bounds(
            value = floor(percentage / max_volume * launchpad_x.LEVELS),
            lower = 0,
            upper = MAX_LEVEL,
            )

    op_list = []
    op_list.append(
            ( columns[0],
                lambda x: x == 0 or x <= LEVEL,
                lambda x: x + 1,
                )
            )

    if len(columns) > 1:
        op_list.append(
            ( columns[1],
                lambda x: x == 0 or x <= LEVEL-1 or (x==MAX_LEVEL and x<=LEVEL),
                lambda x: max(0, x-1 if x != MAX_LEVEL else MAX_LEVEL) + 1,
                )
            )

    for column, get_is_active, get_color_map_index in op_list:
        indices = [(10 + column) + (10*x) for x in range(launchpad_x.LEVELS)]
        for x in indices:
            level_index = floor(x/10) - 1

            is_active = get_is_active(level_index)

            launchpad_x.color_button(
                    byte_signal = ByteMap.Signals.generate_fake_signal(
                        channel = launchpad_x.get_channel(x, is_active),
                        note = x,
                        is_active = is_active,
                        ),
                    color_map = [
                        color_map['levels'][-get_color_map_index(level_index)] if LEVEL>0 else color_map['no-volume'],
                        launchpad_x.COLOR_MAP['default'][1],
                        ],
                    )
