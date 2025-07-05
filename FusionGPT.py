import os
import sys

# Get the absolute path to the "/lib" folder relative to the current file.
lib_path = os.path.join(os.path.dirname(__file__), "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Import the commands module and utilities
from . import commands
from .lib import fusionAddInUtils as futil

# Import FusionGPT class (optional, for advanced features)
try:
    from .lib.FusionGPT import FusionGPT
    FUSIONGPT_AVAILABLE = True
except ImportError as e:
    print(f"FusionGPT class not available: {e}")
    FUSIONGPT_AVAILABLE = False

def run(context):
    try:
        # Initialize FusionGPT if available (optional)
        if FUSIONGPT_AVAILABLE:
            fusiongpt = FusionGPT()
            print("CadxStudio AI Copilot: FusionGPT initialized successfully")
        else:
            print("CadxStudio AI Copilot: Running in basic mode")

        # Start all commands - this is the main functionality
        commands.start()
        print("CadxStudio AI Copilot: Add-in started successfully")

    except Exception as e:
        futil.handle_error('run')
        print(f"CadxStudio AI Copilot: Error during startup: {e}")

def stop(context):
    try:
        # Remove all event handlers
        futil.clear_handlers()

        # Stop all commands
        commands.stop()
        print("CadxStudio AI Copilot: Add-in stopped successfully")

    except Exception as e:
        futil.handle_error('stop')
        print(f"CadxStudio AI Copilot: Error during shutdown: {e}")