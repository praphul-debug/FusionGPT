import json
import math
import re
from typing import Dict, Any, Optional
from ..config import AI_API_KEY, AI_MODEL, AI_MAX_TOKENS, SUPPORTED_AI_COMMANDS

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIService:
    def __init__(self):
        self.client = None
        if OPENAI_AVAILABLE and AI_API_KEY:
            self.client = OpenAI(api_key=AI_API_KEY)
    
    def process_natural_language_command(self, user_input: str) -> Dict[str, Any]:
        """
        Process natural language input and return structured command
        """
        try:
            if self.client:
                return self._process_with_openai(user_input)
            else:
                return self._create_mock_response(user_input)
        except Exception as e:
            return {
                "success": False,
                "error": f"AI processing failed: {str(e)}",
                "action": None,
                "parameters": {}
            }
    
    def _process_with_openai(self, user_input: str) -> Dict[str, Any]:
        """Process command using OpenAI API"""
        system_prompt = f"""
        You are an AI assistant for Fusion 360 CAD software. Convert natural language commands into structured JSON responses.
        
        Available commands: {list(SUPPORTED_AI_COMMANDS.keys())}
        
        Command details:
        {json.dumps(SUPPORTED_AI_COMMANDS, indent=2)}
        
        Rules:
        1. Extract dimensions and convert to millimeters
        2. Use default values if parameters are missing
        3. Return JSON with: action, parameters, success, message
        4. For create_hole, user must select a face first
        5. For extrude_face and move_body, user must select geometry first
        
        Example response:
        {{
            "success": true,
            "action": "create_box",
            "parameters": {{"length": 20, "width": 20, "height": 20}},
            "message": "Creating a 20mm cube"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "success": False,
                    "error": "Could not parse AI response",
                    "action": None,
                    "parameters": {}
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}",
                "action": None,
                "parameters": {}
            }
    
    def _create_mock_response(self, user_input: str) -> Dict[str, Any]:
        """Create mock responses for testing without OpenAI API"""
        user_input = user_input.lower()
        
        # Extract numbers from input
        numbers = re.findall(r'\d+(?:\.\d+)?', user_input)
        
        if 'cube' in user_input or 'box' in user_input:
            size = float(numbers[0]) if numbers else 20
            return {
                "success": True,
                "action": "create_box",
                "parameters": {"length": size, "width": size, "height": size},
                "message": f"Creating a {size}mm cube"
            }
        
        elif 'cylinder' in user_input:
            radius = float(numbers[0]) if numbers else 10
            height = float(numbers[1]) if len(numbers) > 1 else 25
            return {
                "success": True,
                "action": "create_cylinder",
                "parameters": {"radius": radius, "height": height},
                "message": f"Creating cylinder: radius {radius}mm, height {height}mm"
            }
        
        elif 'sphere' in user_input:
            radius = float(numbers[0]) if numbers else 15
            return {
                "success": True,
                "action": "create_sphere",
                "parameters": {"radius": radius},
                "message": f"Creating sphere with radius {radius}mm"
            }
        
        elif 'gear' in user_input:
            teeth = int(numbers[0]) if numbers else 20
            module = float(numbers[1]) if len(numbers) > 1 else 2.0
            bore = float(numbers[2]) if len(numbers) > 2 else 6.0
            thickness = float(numbers[3]) if len(numbers) > 3 else 5.0
            return {
                "success": True,
                "action": "create_gear",
                "parameters": {
                    "number_of_teeth": teeth,
                    "module": module,
                    "bore_diameter": bore,
                    "thickness": thickness
                },
                "message": f"Creating gear: {teeth} teeth, module {module}mm, bore {bore}mm"
            }
        
        elif 'hole' in user_input:
            diameter = float(numbers[0]) if numbers else 5
            depth = float(numbers[1]) if len(numbers) > 1 else 10
            return {
                "success": True,
                "action": "create_hole",
                "parameters": {"diameter": diameter, "depth": depth},
                "message": f"Creating hole: diameter {diameter}mm, depth {depth}mm"
            }
        
        elif 'extrude' in user_input:
            distance = float(numbers[0]) if numbers else 10
            return {
                "success": True,
                "action": "extrude_face",
                "parameters": {"distance": distance},
                "message": f"Extruding selected face by {distance}mm"
            }
        
        elif 'move' in user_input:
            x = float(numbers[0]) if numbers else 10
            y = float(numbers[1]) if len(numbers) > 1 else 0
            z = float(numbers[2]) if len(numbers) > 2 else 0
            return {
                "success": True,
                "action": "move_body",
                "parameters": {"x": x, "y": y, "z": z},
                "message": f"Moving selected body by X:{x}mm, Y:{y}mm, Z:{z}mm"
            }
        
        else:
            return {
                "success": False,
                "error": "Command not recognized. Try: 'create a 20mm cube', 'make a cylinder', 'create gear with 24 teeth'",
                "action": None,
                "parameters": {}
            }