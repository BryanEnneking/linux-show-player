# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
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

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QComboBox, QLabel, \
    QVBoxLayout

from lisp.backends.gst.elements.alsa_sink import AlsaSink
from lisp.backends.gst.settings.settings_page import GstElementSettingsPage


class AlsaSinkSettings(GstElementSettingsPage):

    NAME = "ALSA Sink"
    ELEMENT = AlsaSink

    def __init__(self, element_id, **kwargs):
        super().__init__(element_id)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.devices = self._discover_pcm_devices()
        self.devices['default'] = 'default'

        self.deviceGroup = QGroupBox(self)
        self.deviceGroup.setTitle('ALSA device')
        self.deviceGroup.setGeometry(0, 0, self.width(), 100)
        self.deviceGroup.setLayout(QHBoxLayout())
        self.layout().addWidget(self.deviceGroup)

        self.device = QComboBox(self.deviceGroup)
        self.device.addItems(self.devices.keys())
        self.device.setCurrentText('default')
        self.device.setToolTip('ALSA device, as defined in an asound '
                               'configuration file')
        self.deviceGroup.layout().addWidget(self.device)

        self.label = QLabel('ALSA device', self.deviceGroup)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.deviceGroup.layout().addWidget(self.label)

    def enable_check(self, enable):
        self.deviceGroup.setCheckable(enable)
        self.deviceGroup.setChecked(False)

    def load_settings(self, settings):
        if self.id in settings:
            device = settings[self.id].get('device', 'default')
            for name in self.devices:
                if device == self.devices[name]:
                    self.device.setCurrentText(name)
                    break

    def get_settings(self):
        if not (self.deviceGroup.isCheckable() and not self.deviceGroup.isChecked()):
            return {self.id: {'device': self.devices[self.device.currentText()]}}
        else:
            return {}

    def _discover_pcm_devices(self):
        devices = {}

        with open('/proc/asound/pcm', mode='r') as f:
            for dev in f.readlines():
                dev_name = dev[7:dev.find(':', 7)].strip()
                dev_code = 'hw:' + dev[:5].replace('-', ',')
                devices[dev_name] = dev_code

        return devices
