#!/usr/bin/python
# coding=UTF-8
#
# BitCurator Access Webtools (Disk Image Access for the Web)
# Copyright (C) 2014 - 2016
# All rights reserved.
#
# This code is distributed under the terms of the GNU General Public
# License, Version 3. See the text file "COPYING" for further details
# about the terms of this license.
#
"""Configuration for WikiDP portal Flask app."""
import os
import tempfile
import logging

from flask import Flask

from .const import ConfKey


# Template these values for flexible install
HOST = '0.0.0.0'
TEMP = tempfile.gettempdir()


class BaseConfig():
    """Base / default config, no debug logging and short log format."""
    HOST = HOST
    DEBUG = False
    LOG_FORMAT = '[%(filename)-15s:%(lineno)-5d] %(message)s'
    LOG_FILE = os.path.join(TEMP, 'oauthdemo.log')
    SECRET_KEY = '7d441f27d441f27567d441f2b6176a'


class DevConfig(BaseConfig):
    """Developer level config, with debug logging and long log format."""
    DEBUG = True
    LOG_FORMAT = '[%(asctime)s %(levelname)-8s %(filename)-15s:%(lineno)-5d ' +\
                 '%(funcName)-30s] %(message)s'


CONFIGS = {
    "dev": 'oauthdemo.config.DevConfig',
    "default": 'oauthdemo.config.BaseConfig'
}


def configure_app(app):
    """Grabs the environment variable for app config or defaults to dev."""
    config_name = os.getenv('OAUTHDEMO_CONFIG', 'dev')
    app.config.from_object(CONFIGS[config_name])
    # Bind to PORT if defined, otherwise default to 5000.
    app.config['PORT'] = int(os.environ.get('PORT', 5000))
    app.config['HOST'] = os.environ.get('HOST', HOST)

    # Checking for user-config.py
    try:
        with open('user-config.py'):
            logging.info("user-config.py available")
    except IOError:
        logging.error("user-config.py not available")

APP = Flask(__name__)
# Get the appropriate config
configure_app(APP)
# Configure logging across all modules
logging.basicConfig(filename=APP.config[ConfKey.LOG_FILE], level=logging.DEBUG,
                    format=APP.config[ConfKey.LOG_FORMAT])
logging.info("Started OAuth Demonstrator.")
logging.debug("Configured logging.")
