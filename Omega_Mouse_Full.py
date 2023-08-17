from talon import Context, actions, ctrl, noise
from . import Omega_Mouse


ctx_full = Context()
ctx_full.matches = """
tag: user.om_on
and tag: user.omega_full
"""


# global variable first_pop_done is imported from Omega_Mouse.py to each function with
# "Omega_Mouse.first_pop_done" syntax.


# ========== OMEGA MOUSE - FULL MODE COMMANDS ==========
@ctx_full.action_class('user')
class OmegaMouseFullOverrides:

    # Phase 1: Pop sound enables Gaze control briefly to move cursor > Gaze control disables >
    #          Head tracking enables > global variable set True > Enables tag for 2nd click.
    # Phase 2: Pop sound left clicks > turns off Head tracking > global variable set False >
    #          Removes tag to enable first click again.
    # While Dragging: Popping only moves the cursor to gaze. Does not click.
    def noise_trigger_pop():
        """If no drag, first pop toggles head tracking, second pop confirms click.
        If drag, popping only moves the cursor to gaze."""
        # If drag inactive, popping does 2-phase clicking
        if len(ctrl.mouse_buttons_down()) == 0:
            # Phase 1: Move cursor with gaze then switch to head tracking
            if Omega_Mouse.first_pop_done == False:
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_gaze_toggle(True)
                actions.sleep("50ms")
                actions.tracking.control_gaze_toggle(False)
                actions.sleep("50ms")
                actions.tracking.control_head_toggle(True)
                Omega_Mouse.first_pop_done = True
            # Phase 2: Left click and disable head tracking
            elif Omega_Mouse.first_pop_done == True:
                actions.mouse_click(0)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                Omega_Mouse.first_pop_done = False
        # If drag is active, popping only moves cursor (Phase 1)
        else:
            actions.tracking.control_head_toggle(False)
            actions.tracking.control_gaze_toggle(True)
            actions.sleep("50ms")
            actions.tracking.control_gaze_toggle(False)
            actions.sleep("50ms")
            actions.tracking.control_head_toggle(True)
            Omega_Mouse.first_pop_done = True
            # Setting first_pop_done to True is important while drag is active for a very
            # niche circumstance. If you prefer to hold down a physical button for dragging,
            # instead of using a voice command, once you let go, head tracking will still
            # be active. It makes more sense for Phase 2 to be active at this point,
            # to keep the behavior consistent while head tracking is on.

    def omega_mouse_left_click():
        """Left Click then turn off tracking if needed.
        Alternate way to end Phase 2, or to click immediately without 2-phase popping"""
        if Omega_Mouse.first_pop_done == False:
            actions.mouse_click(0)
        elif Omega_Mouse.first_pop_done == True:
            actions.mouse_click(0)
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
    
    def omega_mouse_left_modup_click():
        """Left Click, release modifer keys, then turn of tracking if needed.
        Alternate way to end Phase 2, or to click immediately without 2-phase popping"""
        if Omega_Mouse.first_pop_done == False:
            actions.mouse_click(0)
            Omega_Mouse.omega_mouse_modifiers_release_function()
        elif Omega_Mouse.first_pop_done == True:
            actions.mouse_click(0)
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
            Omega_Mouse.omega_mouse_modifiers_release_function()

    def omega_mouse_double_click():
        """Double Click that turns off tracking if needed."""
        if Omega_Mouse.first_pop_done == False:
            actions.mouse_click(0)
            actions.mouse_click(0)
        elif Omega_Mouse.first_pop_done == True:
            actions.mouse_click(0)
            actions.mouse_click(0)
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
    
    def omega_mouse_nudge():
        """Skips eye tracking in phase 1. Used to move cursor small distances."""
        # If drag inactive, check first_pop_done
        if len(ctrl.mouse_buttons_down()) == 0:
            if Omega_Mouse.first_pop_done == False:
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(True)
                Omega_Mouse.first_pop_done = True
            elif Omega_Mouse.first_pop_done == True:
                pass
        # If drag is active, do nothing.
        else:
            pass
    
    def omega_mouse_wait():
        """Stops moving cursor. Does not release dragging"""
        if Omega_Mouse.first_pop_done == False:
            pass
        elif Omega_Mouse.first_pop_done == True:
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
    
    # Changes default mouse_drag behavior while Omega Mouse is active to appropriate behavior.
    # Makes dragging end Phase 2, otherwise default action.
    def mouse_drag(button: int):
        """Altered mouse drag for Omega Mouse functionality"""
        if Omega_Mouse.first_pop_done == False:
            """If cursor begins in correct location already, activate drag without move"""
            # stealing drag code from mouse_drag in mouse.py file
            buttons_held_down = list(ctrl.mouse_buttons_down())
            for button in buttons_held_down:
                ctrl.mouse_click(button=button, up=True)
            ctrl.mouse_click(button=button, down=True)
            #----------------------------------------------------
        elif Omega_Mouse.first_pop_done == True:
            """Drag after first pop completes Phase 2. Preps drag for movement"""
            # stealing "drag" code from mouse_drag in mouse.py file
            buttons_held_down = list(ctrl.mouse_buttons_down())
            for button in buttons_held_down:
                ctrl.mouse_click(button=button, up=True)
            ctrl.mouse_click(button=button, down=True)
            #-----------------------------------------
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
    
    # Changes default mouse_drag_end behavior while Omega Mouse is active to appropriate
    # behavior. Completes Phase 2, releases mouse buttons and modifier keys.
    def mouse_drag_end():
        """Completes Phase 2, releases mouse buttons/modifier keys"""
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
        Omega_Mouse.first_pop_done = False
        # stealing "drag end" code from mouse_drag_end function in mouse.py file
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)
        #--------------------------------------------------
        actions.sleep("50ms")
        Omega_Mouse.omega_mouse_modifiers_release_function()
    
