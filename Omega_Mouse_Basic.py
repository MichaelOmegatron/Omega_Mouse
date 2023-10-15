from talon import Context, actions, ctrl, noise
from .Omega_Mouse import omega_mouse_modifiers_release_function, setting_gaze_capture_interval, setting_head_track_lag


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
        gaze_window = setting_gaze_capture_interval.get()
        head_lag = setting_head_track_lag.get()
        actions.tracking.control_head_toggle(False)
        actions.tracking.control_gaze_toggle(True)
        actions.sleep(gaze_window)
        actions.tracking.control_gaze_toggle(False)
        actions.sleep(head_lag)
        actions.tracking.control_head_toggle(True)
        
    def omega_mouse_left_click():
        """Left Click and keep head tracking on. If drag active, drop instead."""
        # If drag is inactive, do left click behavior
        if len(ctrl.mouse_buttons_down()) == 0:
            actions.mouse_click(0)
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(True)
        # If drag is active, do mouse_drag_end instead
        else:
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(True)
            # stealing "drag end" code from mouse_drag_end function in mouse.py file
            buttons_held_down = list(ctrl.mouse_buttons_down())
            for button in buttons_held_down:
                ctrl.mouse_click(button=button, up=True)
            #--------------------------------------------------
            actions.sleep("50ms")
            omega_mouse_modifiers_release_function()
    
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
        
    def omega_mouse_triple_click():
        """Triple Click then keep head tracking on"""
        actions.mouse_click(0)
        actions.mouse_click(0)
        actions.mouse_click(0)
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
    
    def omega_mouse_control_click():
        """Control Click  then keep head tracking on"""
        actions.key("ctrl:down")
        actions.mouse_click(0)
        actions.key("ctrl:up")
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)

    def omega_mouse_shift_click():
        """Shift Click then keep head tracking on"""
        actions.key("shift:down")
        actions.mouse_click(0)
        actions.key("shift:up")
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