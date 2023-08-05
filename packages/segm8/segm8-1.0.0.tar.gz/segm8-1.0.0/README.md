# SegM8Pi

Raspberry Pi library for interaction with a chain of a particular SegM8 7-segment indicator modules.

## Enable SPI Interface

If you haven’t enabled SPI support in your Raspbian Linux yet, open the terminal and run the
following commands:

1. Run `sudo raspi-config`.
2. Use the down arrow to select **5 Interfacing Options**.
3. Arrow down to **P4 SPI**.
4. Select **\<Yes\>** when it asks you to enable SPI.
5. Press **\<Ok\>** when it tells you that SPI is enabled.
6. Use the right arrow to select the **\<Finish\>** button.
7. Reboot your Raspberry Pi to make the SPI interface appear.

After reboot, log in and enter the following command:

```shell
$ ls /dev/spi*
```

The Pi should respond with:

```shell
/dev/spidev0.0  /dev/spidev0.1
```

These represent SPI devices on chip enable pins 0 and 1, respectively. These pins are hardwired
within the Pi.

## Installation

Use **pip** to install the library:

```shell
pip3 install segm8
```

## Quickstart example

```python
import time
import segm8

# Create an object for working with the Segm8 module.
segm8_module = segm8.SegM8(0, 1)

# Display numbers from 0 to 9.
for number in range(10):
    segm8_module.display_int(number, 0, 1)
    time.sleep(1)

# Clear all segments of the module.
segm8_module.clear()
time.sleep(1)

message = "End"
# Display each letter in the message.
for letter in message:
    segm8_module.display_string(letter, 0, 1)
    time.sleep(1)
```

See full [API reference in API.md](https://github.com/amperka/SegM8Pi/blob/master/API.md)
