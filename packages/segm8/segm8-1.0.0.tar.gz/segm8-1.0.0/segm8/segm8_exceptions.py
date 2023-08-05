"""This module describes the exceptions that can be thrown when working
with SegM8 modules."""


class OutOfDeviceRange(Exception):
    """Raise an exception when user data exceeds the number of chained SegM8
    modules."""
    pass


class DataOutOfWidth(Exception):
    """Raise an exception when user data exceeds the required width of the
    elements in the internal buffer."""
    pass


class IncompatibleFlag(Exception):
    """Raise an exception if incompatible flags are used."""
    pass
