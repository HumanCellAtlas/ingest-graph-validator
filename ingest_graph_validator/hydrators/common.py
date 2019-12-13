# -*- coding: utf-8 -*-
"""Common methods used by different hydrators"""


def flatten(d, parent_key=""):
    """
    Flattens a dict

    Flattens a dictionary extending the keys to include the whole path separated by periods. Also stringifies any lists
    inside the dict. Note dict contained inside lists will get stringified without flattening.
    """

    items = []

    for key, value in d.items():
        new_key = parent_key + "." + key if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten(value, new_key).items())
        # Convert inner lists to strings.
        elif isinstance(value, list):
            items.append((new_key, str(value)))
        else:
            items.append((new_key, value))

    return dict(items)
