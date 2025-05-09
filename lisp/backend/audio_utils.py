# This file is part of Linux Show Player
#
# Copyright 2016 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

import math
import wave

# Decibel value to be considered -inf

MIN_VOLUME_DB = -144
# Linear value of MIN_VOLUME_DB
MIN_VOLUME = 6.309_573_444_801_93e-08
# Maximum linear value for the volume, equals to 1000%
MAX_VOLUME = 10
# Decibel value of MAX_VOLUME
MAX_VOLUME_DB = 20


def db_to_linear(value, min_db_zero=True):
    """dB value to linear value conversion."""
    if min_db_zero and value <= MIN_VOLUME_DB:
        return 0

    return 10 ** (value / 20)


def linear_to_db(value):
    """Linear value to dB value conversion."""
    return 20 * math.log10(value) if value > MIN_VOLUME else MIN_VOLUME_DB


def fader_to_slider(value):
    """Inverse function of `slider_to_fader`.

    Note::
        If converting back to an integer scale use `round()` instead of `int()`
    """
    return (value / 3.162_277_66) ** (1 / 3.7)


def slider_to_fader(value):
    """Convert a slider linear value to a fader-like scale.

    The formula used is the following:
        (10db) * (x ^ 3.7)

    Where 10db = 3.16227766
    And 0.0 <= x <= 1.0

    :param value: The value to scale [0-1]
    :type value: float
    """
    if value > 1.0:
        value = 1.0
    elif value < 0.0:
        value = 0

    return 3.162_277_66 * (value**3.7)


def python_duration(path, sound_module):
    """Returns audio-file duration using the given standard library module."""
    duration = 0
    try:
        with sound_module.open(path, "r") as file:
            frames = file.getnframes()
            rate = file.getframerate()
            duration = int(frames / rate * 1000)
    finally:
        return duration


def audio_file_duration(path: str):
    """Return the audio-file duration, using the given file path"""
    return python_duration(path, wave)


def iec_scale(dB):
    """IEC 268-18:1995 standard dB scaling.

    adapted from: http://plugin.org.uk/meterbridge/
    """
    scale = 100

    if dB < -70.0:
        scale = 0.0
    elif dB < -60.0:
        scale = (dB + 70.0) * 0.25
    elif dB < -50.0:
        scale = (dB + 60.0) * 0.50 + 5
    elif dB < -40.0:
        scale = (dB + 50.0) * 0.75 + 7.5
    elif dB < -30.0:
        scale = (dB + 40.0) * 1.5 + 15
    elif dB < -20.0:
        scale = (dB + 30.0) * 2.0 + 30
    elif dB < 0:
        scale = (dB + 20.0) * 2.5 + 50

    return scale / 100
