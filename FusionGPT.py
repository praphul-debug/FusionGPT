import os
import sys

# Get the absolute path to the "/lib" folder relative to the current file.
lib_path = os.path.join(os.path.dirname(__file__), "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusionAddInUtils as futil

from FusionGPT import FusionGPT

def run(context):

    fusiongpt = FusionGPT()

    try:
        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.start()

    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')