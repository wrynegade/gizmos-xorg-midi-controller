def fix_value_to_bounds(value, lower, upper):
    if value < lower:
        return lower
    return upper if value > upper else value
