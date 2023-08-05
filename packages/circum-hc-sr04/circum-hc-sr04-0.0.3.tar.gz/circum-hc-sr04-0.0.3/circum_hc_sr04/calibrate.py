import logging

from Bluetin_Echo import Echo

import click


logger = logging.getLogger(__name__)


@click.option('--trigger-pin',
              required=True,
              type=int,
              help='The pin used to trigger the HC-SR04.')
@click.option('--echo-pin',
              required=True,
              type=int,
              help='The pin the HC-SR04 will signal the echo on.')
@click.option('--samples',
              required=False,
              default=20,
              type=int,
              help='The number of samples to calibrate with.')
@click.option('--distance',
              required=True,
              type=int,
              help='The distance to the calibration object in cm.')
def cli(trigger_pin: int, echo_pin: int, samples: int, distance: int):
    global logger
    logging.basicConfig(level="INFO")
    logger = logging.getLogger("calibrate-hc-sr04")

    echo = Echo(trigger_pin, echo_pin)
    result = echo.calibrate(distance, 'cm', samples)
    print("Calibration complete.\nUse {} m/s as the calibrated speed of sound value.".format(result))


if __name__ == "__main__":
    cli()
