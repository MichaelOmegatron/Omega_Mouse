from talon import Module, actions

mod = Module()

@mod.action_class
class EyeTrackSwitches:
    
    def control_mouse_switch():
        """Toggles Control Mouse on/off"""
        actions.tracking.control_toggle()
        print("Control Mouse toggled")
    
    def zoom_mouse_switch():
        """Toggles Zoom Mouse on/off"""
        actions.tracking.control_zoom_toggle()
        print("Zoom Mouse toggled")

# When I write my ReadMe file, mention that I was advised not to override the tracking
# actions with Contexts due to potential stability issues. This means I had to write new
# methods that need to be placed in the .talon file mouse.py.