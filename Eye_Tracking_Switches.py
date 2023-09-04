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