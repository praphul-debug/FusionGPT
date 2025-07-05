# Application Global Variables
# This module serves as a way to share variables across different
# modules (global variables).

import os

# Flag that indicates to run in Debug mode or not. When running in Debug mode
# more information is written to the Text Command window. Generally, it's useful
# to set this to True while developing an add-in and set it to False when you
# are ready to distribute it.
DEBUG = True

# Gets the name of the add-in from the name of the folder the py file is in.
# This is used when defining unique internal names for various UI elements 
# that need a unique name. It's also recommended to use a company name as 
# part of the ID to better ensure the ID is unique.
ADDIN_NAME = os.path.basename(os.path.dirname(__file__))
COMPANY_NAME = 'CadxStudio'

# Palettes
sample_palette_id = f'{COMPANY_NAME}_{ADDIN_NAME}_palette_id'

# AI Configuration
AI_API_KEY = ""  # Set your OpenAI API key here or leave empty for mock mode
AI_MODEL = "gpt-4"
AI_MAX_TOKENS = 1000

# Supported AI Commands for natural language processing
SUPPORTED_AI_COMMANDS = {
    "create_box": {
        "description": "Creates a rectangular box/cube",
        "parameters": ["length", "width", "height"]
    },
    "create_cylinder": {
        "description": "Creates a cylinder",
        "parameters": ["radius", "height"]
    },
    "create_sphere": {
        "description": "Creates a sphere",
        "parameters": ["radius"]
    },
    "create_gear": {
        "description": "Creates a spur gear with teeth",
        "parameters": ["number_of_teeth", "module", "bore_diameter", "thickness"]
    },
    "create_hole": {
        "description": "Creates a hole in selected face",
        "parameters": ["diameter", "depth"]
    },
    "extrude_face": {
        "description": "Extrudes selected face",
        "parameters": ["distance"]
    },
    "move_body": {
        "description": "Moves selected body",
        "parameters": ["x", "y", "z"]
    }
}