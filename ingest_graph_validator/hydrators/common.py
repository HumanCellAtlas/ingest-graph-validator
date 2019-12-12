import collections


def flatten(d, parent_key=""):
    items = []

    for key, value in d.items():
        new_key = parent_key + "." + key if parent_key else key

        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key).items())
        else:
            items.append((new_key, value))

    return dict(items)
