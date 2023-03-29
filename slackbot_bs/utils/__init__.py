"""Utilities and helper functions."""

import errno
import os
import re
import sys

import slackbot_bs

if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


def env(*vars, **kwargs):
    """This returns the first environment variable set.
    if none are non-empty, defaults to '' or keyword arg default
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get("default", "")


def mkdir_p(path):
    """Make directory and have it work in py2 and py3."""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >= 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]


def end_substr(original, substr):
    """Get the index of the end of the <substr>.

    So you can insert a string after <substr>
    """
    idx = original.find(substr)
    if idx != -1:
        idx += len(substr)
    return idx


def rgb_from_name(name):
    """Create an rgb tuple from a string."""
    hash = 0
    for char in name:
        hash = ord(char) + ((hash << 5) - hash)
    red = hash & 255
    green = (hash >> 8) & 255
    blue = (hash >> 16) & 255
    return red, green, blue


def human_size(bytes, units=None):
    """Returns a human readable string representation of bytes"""
    if not units:
        units = [" bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])


def strfdelta(tdelta, fmt="{hours:{width}}:{minutes:{width}}:{seconds:{width}}"):
    d = {
        "days": tdelta.days,
        "width": "02",
    }
    if tdelta.days > 0:
        fmt = "{days} days " + fmt

    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def flatten_dict(d, parent_key="", sep="."):
    """Flatten a dict to key.key.key = value."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_delta_str(s):
    if "day" in s:
        m = re.match(
            r"(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)",
            s,
        )
    else:
        m = re.match(r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)", s)
    return {key: float(val) for key, val in m.groupdict().items()}
