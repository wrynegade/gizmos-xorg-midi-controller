def create_action_binding(action, action_condition=None, callback=None, **kwargs):
    if callback is None:
        callback = lambda _b : None
    def action_binding(byte_signal):
        if action_condition is None or action_condition(byte_signal):
            action(byte_signal, **kwargs)
        callback(byte_signal)

    return action_binding
