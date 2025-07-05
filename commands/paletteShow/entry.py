import json
import adsk.core
import os
from ...lib import fusionAddInUtils as futil
from ... import config
from ...lib.ai_service import AIService
from ...lib.ai_modeling_actions import AIModelingActions
from datetime import datetime

app = adsk.core.Application.get()
ui = app.userInterface

# Command configuration
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_PalleteShow'
CMD_NAME = 'CadxStudio AI Copilot'
CMD_Description = 'AI-powered natural language 3D modeling for Fusion 360'
PALETTE_NAME = 'CadxStudio AI Copilot'
IS_PROMOTED = True

# Using "global" variables by referencing values from /config.py
PALETTE_ID = config.sample_palette_id

# Specify the full path to the local html
PALETTE_URL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'html', 'index.html')
PALETTE_URL = PALETTE_URL.replace('\\', '/')

# Set a default docking behavior for the palette
PALETTE_DOCKING = adsk.core.PaletteDockingStates.PaletteDockStateRight

# UI configuration
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers
local_handlers = []

# Initialize AI services
ai_service = AIService()
modeling_actions = AIModelingActions()


def start():
    """Executed when add-in is run."""
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Add command created handler
    futil.add_handler(cmd_def.commandCreated, command_created)

    # Add a button into the UI
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)
    control.isPromoted = IS_PROMOTED


def stop():
    """Executed when add-in is stopped."""
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    palette = ui.palettes.itemById(PALETTE_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the Palette
    if palette:
        palette.deleteMe()


def command_created(args: adsk.core.CommandCreatedEventArgs):
    """Event handler for command created event."""
    futil.log(f'{CMD_NAME}: Command created event.')

    # Create the event handlers
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


def command_execute(args: adsk.core.CommandEventArgs):
    """Event handler for command execute event."""
    futil.log(f'{CMD_NAME}: Command execute event.')

    palettes = ui.palettes
    palette = palettes.itemById(PALETTE_ID)
    
    if palette is None:
        palette = palettes.add(
            id=PALETTE_ID,
            name=PALETTE_NAME,
            htmlFileURL=PALETTE_URL,
            isVisible=True,
            showCloseButton=True,
            isResizable=True,
            width=400,
            height=800,
            useNewWebBrowser=True
        )
        futil.add_handler(palette.closed, palette_closed)
        futil.add_handler(palette.navigatingURL, palette_navigating)
        futil.add_handler(palette.incomingFromHTML, palette_incoming)
        futil.log(f'{CMD_NAME}: Created new palette: ID = {palette.id}, Name = {palette.name}')

    if palette.dockingState == adsk.core.PaletteDockingStates.PaletteDockStateFloating:
        palette.dockingState = PALETTE_DOCKING

    palette.isVisible = True


def palette_closed(args: adsk.core.UserInterfaceGeneralEventArgs):
    """Handle palette closed event."""
    futil.log(f'{CMD_NAME}: Palette was closed.')


def palette_navigating(args: adsk.core.NavigationEventArgs):
    """Handle palette navigation event."""
    futil.log(f'{CMD_NAME}: Palette navigating event.')

    url = args.navigationURL
    futil.log(f"User is attempting to navigate to {url}", adsk.core.LogLevels.InfoLogLevel)

    # Check if url is an external site and open in user's default browser
    if url.startswith("http"):
        args.launchExternally = True


def palette_incoming(html_args: adsk.core.HTMLEventArgs):
    """Handle events sent from JavaScript in the palette."""
    futil.log(f'{CMD_NAME}: Palette incoming event.')

    try:
        message_data: dict = json.loads(html_args.data)
        message_action = html_args.action

        log_msg = f"Event received from {html_args.firingEvent.sender.name}\n"
        log_msg += f"Action: {message_action}\n"
        log_msg += f"Data: {message_data}"
        futil.log(log_msg, adsk.core.LogLevels.InfoLogLevel)

        # Handle AI command processing
        if message_action == 'processAICommand':
            response = process_ai_command(message_data)
            html_args.returnData = json.dumps(response)
            return

        # Handle legacy message from palette
        elif message_action == 'messageFromPalette':
            arg1 = message_data.get('arg1', 'arg1 not sent')
            arg2 = message_data.get('arg2', 'arg2 not sent')

            msg = 'An event has been fired from the html to Fusion with the following data:<br/>'
            msg += f'<b>Action</b>: {message_action}<br/><b>arg1</b>: {arg1}<br/><b>arg2</b>: {arg2}'               
            ui.messageBox(msg)

        # Return timestamp
        now = datetime.now()
        currentTime = now.strftime('%H:%M:%S')
        html_args.returnData = f'OK - {currentTime}'

    except Exception as e:
        error_msg = f"Error processing palette message: {str(e)}"
        futil.log(error_msg, adsk.core.LogLevels.ErrorLogLevel)
        html_args.returnData = json.dumps({
            "success": False,
            "error": error_msg
        })


def process_ai_command(message_data: dict) -> dict:
    """Process AI command and execute in Fusion 360."""
    try:
        command = message_data.get('command', '').strip()
        
        if not command:
            return {
                "success": False,
                "error": "No command provided"
            }

        futil.log(f"Processing AI command: {command}")

        # Step 1: Process natural language with AI
        ai_response = ai_service.process_natural_language_command(command)
        
        if not ai_response.get('success', False):
            return {
                "success": False,
                "error": ai_response.get('error', 'AI processing failed')
            }

        action = ai_response.get('action')
        parameters = ai_response.get('parameters', {})
        
        futil.log(f"AI interpreted action: {action}, parameters: {parameters}")

        # Step 2: Execute the modeling action
        execution_result = modeling_actions.execute_command(action, parameters)
        
        if execution_result.get('success', False):
            return {
                "success": True,
                "message": execution_result.get('message', 'Command executed successfully'),
                "action": action,
                "parameters": parameters
            }
        else:
            return {
                "success": False,
                "error": execution_result.get('message', 'Execution failed')
            }

    except Exception as e:
        error_msg = f"Error processing AI command: {str(e)}"
        futil.log(error_msg, adsk.core.LogLevels.ErrorLogLevel)
        return {
            "success": False,
            "error": error_msg
        }


def command_destroy(args: adsk.core.CommandEventArgs):
    """Event handler for command destroy event."""
    futil.log(f'{CMD_NAME}: Command destroy event.')

    global local_handlers
    local_handlers = []