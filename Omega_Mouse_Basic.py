from talon import Context, actions, ctrl, noise
from .Omega_Mouse import omega_mouse_modifiers_release_function


ctx_basic = Context()
ctx_basic.matches = """
tag: user.om_on
and tag: user.omega_basic
"""


# ========== OMEGA MOUSE - BASIC MODE COMMANDS ==========
@ctx_basic.action_class('user')
class OmegaMouseBasicOverrides:

    def noise_trigger_pop():
        """Move cursor to gaze then switch to head tracking."""
        actions.tracking.control_head_toggle(False)
        actions.tracking.control_gaze_toggle(True)
        actions.sleep("50ms")
        actions.tracking.control_gaze_toggle(False)
        actions.sleep("50ms")
        actions.tracking.control_head_toggle(True)
        
    def omega_mouse_left_click():
        """Left Click then turn off tracking"""
        actions.mouse_click(0)
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
    
    def omega_mouse_left_modup_click():
        """Left Click, release modifer keys, keep head tracking on"""
        actions.mouse_click(0)
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
        omega_mouse_modifiers_release_function()
    
    def omega_mouse_double_click():
        """Double Click then keep head tracking on"""
        actions.mouse_click(0)
        actions.mouse_click(0)
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
        
    def omega_mouse_relocate():
        """Does nothing in Basic Mode"""
        print("Does nothing in Basic Mode.")
            
    def omega_mouse_wait():
        """Stops moving the cursor. Does not release dragging."""
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)

    # Changes default mouse_drag behavior while Omega Mouse is active to appropriate behavior.
    def mouse_drag(button: int):
        """Altered mouse drag for Omega Mouse functionality"""
        # stealing drag code from mouse_drag in mouse.py file
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)
        ctrl.mouse_click(button=button, down=True)
        #-----------------------------------------
        actions.tracking.control_gaze_toggle(False)
        actions.sleep("50ms")
        actions.tracking.control_head_toggle(True)
    
    # Changes default mouse_drag_end behavior while Omega Mouse is active to appropriate
    # behavior. Releases mouse buttons and modifier keys.
    def mouse_drag_end():
        """Altered mouse_drag_end for Omega Mouse functionality"""
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
        # stealing "drag end" code from mouse_drag_end function in mouse.py file
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)
        #--------------------------------------------------
        actions.sleep("50ms")
        omega_mouse_modifiers_release_function()