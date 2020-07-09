# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge.readthedocs.io/
# FLEDGE_END

from coral.enviro.board import EnviroBoard
import copy
import logging

from fledge.common import logger
from fledge.plugins.common import utils
from fledge.services.south import exceptions

__author__ = "Charlie Wang"
__copyright__ = "Copyright 2020 Google Inc."
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_DEFAULT_CONFIG = {
    'plugin': {
         'description': 'Coral Environmental Sensor Board Poll Plugin',
         'type': 'string',
         'default': 'coral-enviro',
         'readonly': 'true'
    },
    'assetName': {
        'description': 'Name of Asset',
        'type': 'string',
        'default': 'enviro',
        'displayName': 'Asset name',
        'mandatory': 'true',
        'order': '2',
    },
    'temperatureSensor': {
        'description': 'Enable Temperature sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '3',
        'displayName': 'Temperature Sensor'
    },
    'pressureSensor': {
        'description': 'Enable Barometric Pressure sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '4',
        'displayName': 'Pressure Sensor'
    },
    'humiditySensor': {
        'description': 'Enable Humidity sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '5',
        'displayName': 'Humidity Sensor'
    },
    'ambientLightSensor': {
        'description': 'Enable Ambient Light sensor',
        'type': 'boolean',
        'default': 'true',
        'order': '6',
        'displayName': 'Ambient Light Sensor'
    },
    'groveAnalogSensor': {
        'description': 'Enable Grove Analog sensor',
        'type': 'boolean',
        'default': 'false',
        'order': '7',
        'displayName': 'Grove Analog Sensor'
    }
}

_LOGGER = logger.setup(__name__, level=logging.INFO)

""" Setup the access to the logging system of Fledge """

_enviro = None

def plugin_info():
    return {
        'name': 'Coral Environmental Sensor Board',
        'version': '1.8.1',
        'mode': 'poll',
        'type': 'south',
        'interface': '1.0',
        'config': _DEFAULT_CONFIG
    }

def plugin_init(config):
    data = copy.deepcopy(config)
    _LOGGER.info("Config for coral-enviro plugin {}".format(config))
    global _enviro
    _enviro = EnviroBoard() 
    _LOGGER.info("Init coral-enviro plugin complete")
    return data

def plugin_poll(handle):
    _LOGGER.debug("coral-enviro plugin_poll")
    global _enviro
    try:
        time_stamp = utils.local_timestamp()
        readings = {}
        if handle['temperatureSensor']['value'] == 'true':
            readings['temperature'] = _enviro.temperature

        if handle['pressureSensor']['value'] == 'true':
            readings['pressure'] = _enviro.pressure

        if handle['humiditySensor']['value'] == 'true':
            readings['humidity'] = _enviro.humidity

        if handle['ambientLightSensor']['value'] == 'true':
            readings['ambient_light'] = _enviro.ambient_light

        if handle['groveAnalogSensor']['value'] == 'true':
            readings['grove_analog'] = _enviro.grove_analog

        wrapper = {
                'asset':     handle['assetName']['value'],
                'timestamp': time_stamp,
                'readings':  readings
        }
        return wrapper
    except Exception as ex:
        _LOGGER.exception("coral-enviro exception: {}".format(str(ex)))
        raise exceptions.DataRetrievalError(ex)

def plugin_reconfigure(handle, new_config):
    new_handle = copy.deepcopy(new_config)
    return new_handle

def plugin_shutdown(handle):
    pass
