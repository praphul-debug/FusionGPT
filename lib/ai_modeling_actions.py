import adsk.core
import adsk.fusion
import math
from typing import Dict, Any

app = adsk.core.Application.get()

class AIModelingActions:
    def __init__(self):
        self.app = app
        self.ui = app.userInterface
    
    def execute_command(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the AI-interpreted command in Fusion 360"""
        try:
            if action == "create_box":
                return self._create_box(parameters)
            elif action == "create_cylinder":
                return self._create_cylinder(parameters)
            elif action == "create_sphere":
                return self._create_sphere(parameters)
            elif action == "create_gear":
                return self._create_gear(parameters)
            elif action == "create_hole":
                return self._create_hole(parameters)
            elif action == "extrude_face":
                return self._extrude_face(parameters)
            elif action == "move_body":
                return self._move_body(parameters)
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
    
    def _create_box(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a box/cube"""
        try:
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Get parameters with defaults
            length = params.get('length', 20) / 10  # Convert mm to cm
            width = params.get('width', 20) / 10
            height = params.get('height', 20) / 10
            
            # Create sketch
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            # Draw rectangle
            lines = sketch.sketchCurves.sketchLines
            rect = lines.addTwoPointRectangle(
                adsk.core.Point3D.create(-length/2, -width/2, 0),
                adsk.core.Point3D.create(length/2, width/2, 0)
            )
            
            # Create extrusion
            prof = sketch.profiles.item(0)
            extrudes = rootComp.features.extrudeFeatures
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(height)
            extInput.setDistanceExtent(False, distance)
            extrude = extrudes.add(extInput)
            
            return {
                "success": True,
                "message": f"Created box: {params.get('length', 20)}×{params.get('width', 20)}×{params.get('height', 20)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create box: {str(e)}"
            }
    
    def _create_cylinder(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a cylinder"""
        try:
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Get parameters with defaults
            radius = params.get('radius', 10) / 10  # Convert mm to cm
            height = params.get('height', 25) / 10
            
            # Create sketch
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            # Draw circle
            circles = sketch.sketchCurves.sketchCircles
            centerPoint = adsk.core.Point3D.create(0, 0, 0)
            circle = circles.addByCenterRadius(centerPoint, radius)
            
            # Create extrusion
            prof = sketch.profiles.item(0)
            extrudes = rootComp.features.extrudeFeatures
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(height)
            extInput.setDistanceExtent(False, distance)
            extrude = extrudes.add(extInput)
            
            return {
                "success": True,
                "message": f"Created cylinder: radius {params.get('radius', 10)}mm, height {params.get('height', 25)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create cylinder: {str(e)}"
            }
    
    def _create_sphere(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a sphere"""
        try:
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Get parameters with defaults
            radius = params.get('radius', 15) / 10  # Convert mm to cm
            
            # Create sketch for revolve
            sketches = rootComp.sketches
            xzPlane = rootComp.xZConstructionPlane
            sketch = sketches.add(xzPlane)
            
            # Draw semicircle
            arcs = sketch.sketchCurves.sketchArcs
            centerPoint = adsk.core.Point3D.create(0, 0, 0)
            startPoint = adsk.core.Point3D.create(0, 0, radius)
            endPoint = adsk.core.Point3D.create(0, 0, -radius)
            arc = arcs.addByCenterStartEnd(centerPoint, startPoint, endPoint)
            
            # Add line to close profile
            lines = sketch.sketchCurves.sketchLines
            line = lines.addByTwoPoints(startPoint, endPoint)
            
            # Create revolve
            prof = sketch.profiles.item(0)
            revolves = rootComp.features.revolveFeatures
            revInput = revolves.createInput(prof, line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            angle = adsk.core.ValueInput.createByReal(math.pi * 2)
            revInput.setAngleExtent(False, angle)
            revolve = revolves.add(revInput)
            
            return {
                "success": True,
                "message": f"Created sphere: radius {params.get('radius', 15)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create sphere: {str(e)}"
            }
    
    def _create_gear(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a spur gear with actual teeth"""
        try:
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Get parameters with defaults
            num_teeth = params.get('number_of_teeth', 20)
            module = params.get('module', 2.0) / 10  # Convert mm to cm
            bore_diameter = params.get('bore_diameter', 6.0) / 10
            thickness = params.get('thickness', 5.0) / 10
            
            # Calculate gear dimensions
            pitch_diameter = num_teeth * module
            outer_diameter = pitch_diameter + (2 * module)
            root_diameter = pitch_diameter - (2.5 * module)
            
            # Create sketch
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            
            # Draw gear profile
            lines = sketch.sketchCurves.sketchLines
            arcs = sketch.sketchCurves.sketchArcs
            
            # Create simplified gear teeth using lines
            angle_per_tooth = 2 * math.pi / num_teeth
            tooth_width_angle = angle_per_tooth * 0.4  # 40% of tooth pitch for tooth width
            
            points = []
            
            for i in range(num_teeth):
                base_angle = i * angle_per_tooth
                
                # Tooth tip points
                tip_angle1 = base_angle - tooth_width_angle / 2
                tip_angle2 = base_angle + tooth_width_angle / 2
                
                # Root points
                root_angle1 = base_angle + tooth_width_angle / 2
                root_angle2 = base_angle + angle_per_tooth - tooth_width_angle / 2
                
                # Add points for this tooth
                points.extend([
                    adsk.core.Point3D.create(
                        (outer_diameter / 2) * math.cos(tip_angle1),
                        (outer_diameter / 2) * math.sin(tip_angle1),
                        0
                    ),
                    adsk.core.Point3D.create(
                        (outer_diameter / 2) * math.cos(tip_angle2),
                        (outer_diameter / 2) * math.sin(tip_angle2),
                        0
                    ),
                    adsk.core.Point3D.create(
                        (root_diameter / 2) * math.cos(root_angle1),
                        (root_diameter / 2) * math.sin(root_angle1),
                        0
                    ),
                    adsk.core.Point3D.create(
                        (root_diameter / 2) * math.cos(root_angle2),
                        (root_diameter / 2) * math.sin(root_angle2),
                        0
                    )
                ])
            
            # Draw the gear outline
            for i in range(len(points)):
                next_i = (i + 1) % len(points)
                lines.addByTwoPoints(points[i], points[next_i])
            
            # Add center bore hole
            if bore_diameter > 0:
                circles = sketch.sketchCurves.sketchCircles
                centerPoint = adsk.core.Point3D.create(0, 0, 0)
                bore_circle = circles.addByCenterRadius(centerPoint, bore_diameter / 2)
            
            # Create extrusion
            profiles = sketch.profiles
            gear_profile = None
            
            # Find the gear profile (largest area)
            max_area = 0
            for profile in profiles:
                if profile.areaProperties().area > max_area:
                    max_area = profile.areaProperties().area
                    gear_profile = profile
            
            if gear_profile:
                extrudes = rootComp.features.extrudeFeatures
                extInput = extrudes.createInput(gear_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                distance = adsk.core.ValueInput.createByReal(thickness)
                extInput.setDistanceExtent(False, distance)
                extrude = extrudes.add(extInput)
            
            return {
                "success": True,
                "message": f"Created gear: {num_teeth} teeth, module {params.get('module', 2.0)}mm, bore {params.get('bore_diameter', 6.0)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create gear: {str(e)}"
            }
    
    def _create_hole(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a hole in selected face"""
        try:
            # Get parameters
            diameter = params.get('diameter', 5) / 10  # Convert mm to cm
            depth = params.get('depth', 10) / 10
            
            # Check if a face is selected
            selection = self.ui.activeSelections
            if selection.count == 0:
                return {
                    "success": False,
                    "message": "Please select a face first before creating a hole"
                }
            
            selected_face = selection.item(0).entity
            if not isinstance(selected_face, adsk.fusion.BRepFace):
                return {
                    "success": False,
                    "message": "Please select a face to create the hole"
                }
            
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Create sketch on selected face
            sketches = rootComp.sketches
            sketch = sketches.add(selected_face)
            
            # Get face center point (simplified)
            centerPoint = selected_face.pointOnFace
            sketch_point = sketch.modelToSketchSpace(centerPoint)
            
            # Draw circle
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(sketch_point, diameter / 2)
            
            # Create cut extrusion
            prof = sketch.profiles.item(0)
            extrudes = rootComp.features.extrudeFeatures
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(depth)
            extInput.setDistanceExtent(False, distance)
            extrude = extrudes.add(extInput)
            
            return {
                "success": True,
                "message": f"Created hole: diameter {params.get('diameter', 5)}mm, depth {params.get('depth', 10)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create hole: {str(e)}"
            }
    
    def _extrude_face(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extrude selected face"""
        try:
            distance = params.get('distance', 10) / 10  # Convert mm to cm
            
            # Check if a face is selected
            selection = self.ui.activeSelections
            if selection.count == 0:
                return {
                    "success": False,
                    "message": "Please select a face first before extruding"
                }
            
            selected_face = selection.item(0).entity
            if not isinstance(selected_face, adsk.fusion.BRepFace):
                return {
                    "success": False,
                    "message": "Please select a face to extrude"
                }
            
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Create extrusion from face
            extrudes = rootComp.features.extrudeFeatures
            extInput = extrudes.createInput(selected_face, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            distance_input = adsk.core.ValueInput.createByReal(distance)
            extInput.setDistanceExtent(False, distance_input)
            extrude = extrudes.add(extInput)
            
            return {
                "success": True,
                "message": f"Extruded face by {params.get('distance', 10)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to extrude face: {str(e)}"
            }
    
    def _move_body(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Move selected body"""
        try:
            x = params.get('x', 0) / 10  # Convert mm to cm
            y = params.get('y', 0) / 10
            z = params.get('z', 0) / 10
            
            # Check if a body is selected
            selection = self.ui.activeSelections
            if selection.count == 0:
                return {
                    "success": False,
                    "message": "Please select a body first before moving"
                }
            
            selected_body = selection.item(0).entity
            if not isinstance(selected_body, adsk.fusion.BRepBody):
                return {
                    "success": False,
                    "message": "Please select a body to move"
                }
            
            design = app.activeProduct
            rootComp = design.rootComponent
            
            # Create move feature
            moveFeats = rootComp.features.moveFeatures
            moveInput = moveFeats.createInput(adsk.core.ObjectCollection.create())
            moveInput.inputEntities.add(selected_body)
            
            # Create transform
            vector = adsk.core.Vector3D.create(x, y, z)
            transform = adsk.core.Matrix3D.create()
            transform.translation = vector
            moveInput.transform = transform
            
            moveFeature = moveFeats.add(moveInput)
            
            return {
                "success": True,
                "message": f"Moved body by X:{params.get('x', 0)}mm, Y:{params.get('y', 0)}mm, Z:{params.get('z', 0)}mm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to move body: {str(e)}"
            }