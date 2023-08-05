"""The module contains the SegM8 class that allows you to interact with
a chain of a particular SegM8 7-segment indicator modules.
This module requires that `spidev` be installed within the Python
environment you are using it.
"""

import spidev
from . import font
from .output_format import Align, NumberSystem
from .segm8_exceptions import (
    DataOutOfWidth,
    OutOfDeviceRange,
    IncompatibleFlag,
)


class SegM8:

    """Class for SegM8 7-segment module."""

    def __init__(self, pin_CE, device_count=1):
        """The constructor for SegM8 class.

        Parameters:
        -----------
        pin_CE: int
            The chip enable (also known as chip select or slave select)
            pin used to control the shift-register latch. It can take
            the values 0 or 1, which corresponds to the CE0 or CE1 pins
            on the Raspberry Pi board.
        device_count: int
            The number of SegM8 modules connected in a daisy-chain. If
            omitted, defines a single module.
        """
        self._pin_CE = pin_CE
        self._device_count = device_count
        # Create an SPI object on the "0" SPI bus and connected to
        # "pin_CE".
        self._spi = self._spi_init(0, self._pin_CE)
        # Set the internal buffer to the "dark" state.
        self._data = [font.FONT[" "]] * self._device_count
        self._send_data()

    def clear(self):
        """Sets all module segments to the "dark" state. Clear the
        internal buffer.

        Returns:
        --------
        None
        """
        self._data = [font.FONT[" "]] * self._device_count
        self._send_data()

    def display_int(
        self,
        number,
        position,
        width,
        align=Align.RIGHT,
        pad_zeros=False,
        radix=NumberSystem.DEC,
    ):
        """Prints a number of a fixed width starting with the position
        to the output buffer using formatting flags.

        Parameters:
        -----------
        number: int
            An integer to be displayed.
        position: int
            The starting position of the output of a number in the
            internal buffer.
        width: int
            The number of elements in the internal buffer, and
            accordingly the number of SegM8 modules needed to display
            a number.

        Optional parameters:
        --------------------
        align: int
            Output alignment method. segm8.Align.RIGHT – align to the
            right corner, segm8.Align.LEFT – align to the left corner.
        pad_zeros: bool
            Add leading zeros before the number. Compatible only with
            segm8.Align.RIGHT.
        radix: int
            Number system. Determines in which number system the output
            will be presented: segm8.NumberSystem.DEC – decimal,
            segm8.NumberSystem.HEX – hexadecimal (compatible only with
            non-negative numbers).

        Returns:
        --------
        None
        """
        if radix == NumberSystem.DEC:
            split_number = list(str(number))
        elif radix == NumberSystem.HEX and number >= 0:
            # Remove "0x" from sequence.
            split_number = list(hex(number)[2:])
            for i, char in enumerate(split_number):
                # Chars "a", "e", "f" must be in upper case according to
                # the font.
                if char in ("a", "e", "f"):
                    split_number[i] = char.upper()
        elif radix == NumberSystem.HEX and number < 0:
            raise IncompatibleFlag(
                'The "NumberSystem.HEX" parameter is incompatible with a '
                + "negative number."
            )
        placeholder = "0" if pad_zeros and align == Align.RIGHT else " "
        self._display(split_number, position, width, align, placeholder)

    def display_float(
        self,
        number,
        position,
        width,
        precision=1,
        align=Align.LEFT,
        pad_zeros=False,
    ):
        """Prints a number of type float of a fixed width starting with
        the position to the output buffer using formatting flags.

        Parameters:
        -----------
        number: float
            The floating point number to be displayed.
        position: int
            The starting position of the output of a number in the
            internal buffer.
        width: int
            The number of elements in the internal buffer, and
            accordingly the number of SegM8 modules needed to display
            a number.

        Optional parameters:
        --------------------
        precision: int
            Decimal places count of float.
        align: int
            Output alignment method. segm8.Align.RIGHT – align to the
            right corner, segm8.Align.LEFT – align to the left corner.
        pad_zeros: bool
            Add leading zeros before the number. Compatible only with
            segm8.Align.RIGHT.

        Returns:
        --------
        None
        """
        format_spec = "".join([".", str(precision), "f"])
        split_number = list(format(number, format_spec))
        placeholder = "0" if pad_zeros and align == Align.RIGHT else " "
        self._display(split_number, position, width, align, placeholder)

    def display_string(self, string, position, width, align=Align.LEFT):
        """Prints a string of a fixed width starting with the position
        to the output buffer using formatting flags. Moves the contents
        of the buffer to the indicator daisy-chain. Note: the "." sign
        does not occupy a  separate module and is displayed with the
        previous character.

        Parameters:
        -----------
        string: str
            Text line.
        position: int
            The starting position of the output of a string in the
            internal buffer.
        width: int
            The number of elements in the internal buffer, and
            accordingly the number of SegM8 modules needed to display
            a number or a text.

        Optional parameters:
        --------------------
        align: int
            Output alignment method. "segm8.Align.RIGHT" – align to the
            right corner, "segm8.Align.LEFT" – align to the left corner.

        Returns:
        --------
        None
        """
        split_string = list(string)
        self._display(split_string, position, width, align)

    def write_segments(self, mask, device_index):
        """Displays a custom symbol in the specified position.

        Parameters:
        -----------
        mask: int
            list of boolean values for all 8 segments. The ordinal
            number of the member of this list corresponds to the letter
            index of a indicator segment: 0-a, 1-b, <...>, 7-h(dot).
        device_index: int
            A SegM8 device ordinal number in the daisy-chain. Can be in
            the range [0 .. device_count - 1].

        Returns:
        --------
        None
        """
        for i, val in enumerate(mask):
            if val:
                self._data[device_index] |= (1 << i) & 0xFF
            else:
                self._data[device_index] &= ~(1 << i) & 0xFF

        self._send_data()

    def __del__(self):
        """The destructor is used to set all segments of all modules to
        the "dark" state and to close the SPI connection."""
        self._data = [font.FONT[" "]] * self._device_count
        self._send_data()
        self._spi.close()

    def _spi_init(self, bus, pin_CE):
        """Returns a new SPI object that is connected to the specified
        SPI device interface.

        Parameters:
        -----------
        bus: int
            SPI bus number.
        pin_CE: int
            The chip enable pin.

        Returns:
        --------
        SpiDev object
        """
        spi = spidev.SpiDev()
        spi.open(bus, pin_CE)
        spi.max_speed_hz = 4000000
        spi.mode = 0
        return spi

    def _save_data(self, data, position, width):
        """Saves a list of data to an internal buffer.

        Parameters:
        -----------
        data: List[int]
            List of data to be saved to the internal buffer.
        position: int
            The starting position of the data in the internal buffer.
        width: int
            The number of elements in the internal buffer, and
            accordingly the number of SegM8 modules needed to display
            a number or a text.

        Returns:
        --------
        None
        """
        if (
            len(data) > self._device_count
            or position + width > self._device_count
        ):
            raise OutOfDeviceRange("Output out of range of connected devices.")

        self._data[position: position + width] = data

    def _send_data(self):
        """Sends the contents of the internal buffer over the SPI
        interface to the chained SegM8 modules.

        Returns:
        --------
        None
        """
        self._spi.writebytes(self._data[::-1])

    def _display(self, raw_data, position, width, align, placeholder=" "):
        """Formats the input data, stores it in an internal buffer, and
        sends it to the chained SegM8 modules.

        Parameters:
        -----------
        raw_data: List[str]
            Raw data to be formatted.
        position: int
            The starting position of the data in the internal buffer.
        width: int
            The number of elements in the internal buffer, and
            accordingly the number of SegM8 modules needed to display
            a number or a text.

        Returns:
        --------
        None
        """
        format_data = create_format_data(raw_data, width, align, placeholder)
        self._save_data(format_data, position, width)
        self._send_data()


def align_data(sequence, align, placeholder, count):
    """Adds the specified count of placeholders to the right or left of
    the sequence. (changes the input sequence.)

    Parameters:
    -----------
    sequence: List[int]
        Input sequence of integers.
    align: int
        Output alignment method. Align.RIGHT – align to the right
        corner, Align.LEFT – align to the left corner.
    placeholder: int
        A placeholder to add to the sequence.
    count: int
        The number of placeholders to add.

    Returns:
    --------
    None
    """
    pad = [placeholder] * count
    if align == Align.LEFT:
        sequence.extend(pad)
    elif align == Align.RIGHT:
        sequence[:0] = pad


def create_format_data(raw_data, width, align, placeholder=" "):
    """Creates a list from the raw data, formatted with an applicable
    font and alignment method. The width of the formatted data is
    limited by the "width" parameter. If it exceeds the specified
    "width" parameter, a DataOutOfWidth exception is thrown.

    Parameters:
    -----------
    raw_data: List[str]
        List of string data to be formatted.
    width: int
        The number of elements in the internal buffer, and
        accordingly the number of SegM8 modules needed to display
        a number or a text.
    align: int
        Output alignment method. Align.RIGHT – align to the right
        corner, Align.LEFT – align to the left corner.

    Optional parameter:
    -------------------
    placeholder: str
        Placeholder added to formatted data.

    Returns:
    --------
    List[int]
    """
    format_data = [font.FONT.get(val, font.FONT["DFLT"]) for val in raw_data]
    if font.FONT["."] in format_data:
        dot_indexes = []
        for index, data in enumerate(format_data):
            if (
                data == font.FONT["."]
                and index != 0
                and format_data[index - 1] != font.FONT["."]
            ):
                dot_indexes.append(index)
                format_data[index - 1] |= font.FONT["."]
        for index in sorted(dot_indexes, reverse=True):
            del format_data[index]

    if len(format_data) < width:
        place_count = width - len(format_data)
        align_data(format_data, align, font.FONT[placeholder], place_count)
    elif len(format_data) > width:
        raise DataOutOfWidth(
            "The data length exceeds the entered output width."
        )
    return format_data
