def map_dict(list_):
    i = 1
    mapped = {}
    for item in list_:
        mapped[i] = item
        i += 1
    return mapped


def input_int(message, limit, exceptions=()):
    while True:
        try:
            val = input(message)
            if val in exceptions:
                return val
            val = int(val)
            if not (0 < val <= limit):
                print("Invalid input. Please try again.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please try again.")
