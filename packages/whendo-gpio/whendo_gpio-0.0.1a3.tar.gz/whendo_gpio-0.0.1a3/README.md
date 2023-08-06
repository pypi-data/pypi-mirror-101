# whendo_gpio

whendo_gpio adds Raspberry Pi GPIO Actions to a whendo installation. See whendo_gpio/action.py for GPIO Actions.

If running on a Raspberry Pi, be sure to install RPi.GPIO. Also install psutil if you want additional system information to be available through
the SysInfo Action.

The Mock.GPIO library is useful for running Jupyter notebooks and other runtimes (on non-Raspberry Pi computers) that create and manage Actions, Schedulers, and Programs destined for Raspberry Pi deployments.

## Dependencies

- install_requires =
    whendo >= 0.0.2a27
    Mock.GPIO >= 0.1.8

## Computers tested (so far):

- 32-bit Raspberry Pi OS [pi 3B+, pi 4B]
- 64-bit Intel MacOS