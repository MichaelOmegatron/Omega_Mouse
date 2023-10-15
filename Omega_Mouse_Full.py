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
        gaze_window = Omega_Mouse.setting_gaze_capture_interval.get()
        head_lag = Omega_Mouse.setting_head_track_lag.get()
        # If drag inactive, popping does 2-phase clicking
        if len(ctrl.mouse_buttons_down()) == 0:
            # Phase 1: Move cursor with gaze then switch to head tracking
            if Omega_Mouse.first_pop_done == False:
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_gaze_toggle(True)
                actions.sleep(gaze_window)
                actions.tracking.control_gaze_toggle(False)
                actions.sleep(head_lag)
                actions.tracking.control_head_toggle(True)
                Omega_Mouse.first_pop_done = True
            # Phase 2: Left click and disable head tracking
            elif Omega_Mouse.first_pop_done == True:
                actions.mouse_click(0)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                Omega_Mouse.first_pop_done = False
        # If drag is active, Phase 2 pop does "mouse_drag_end" instead of simple left click
        else:
            if Omega_Mouse.first_pop_done == False:
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_gaze_toggle(True)
                actions.sleep(gaze_window)
                actions.tracking.control_gaze_toggle(False)
                actions.sleep(head_lag)
                actions.tracking.control_head_toggle(True)
                Omega_Mouse.first_pop_done = True
            # Second pop does "mouse_drag_end" in ctx_full below
            elif Omega_Mouse.first_pop_done == True:
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
            # Note: If you have mouse drag mapped to a physical switch, the code will recognize
            # the drag state, but the first_pop_done variable will not update. For example,
            # if you pop the cursor over to an item, activate your drag command with a switch,
            # you will need to use the "relo" command to move the cursor, because the next pop
            # you make will instead activate the "mouse_drag_end" command.
            
    def omega_mouse_left_click():
        """Left Click then turn off tracking if needed. If drag held, drop instead.
        Alternate way to end Phase 2, or to click immediately without 2-phase popping"""
        # If drag is inactive, check first_pop_done for left click behavior.
        if len(ctrl.mouse_buttons_down()) == 0:
            if Omega_Mouse.first_pop_done == False:
                actions.mouse_click(0)
            elif Omega_Mouse.first_pop_done == True:
                actions.mouse_click(0)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                Omega_Mouse.first_pop_done = False
        # If drag is active, do mouse_drag_end instead
        else:
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

    def omega_mouse_triple_click():
        """Triple Click that turns off tracking if needed."""
        if Omega_Mouse.first_pop_done == False:
            actions.mouse_click(0)
            actions.mouse_click(0)
            actions.mouse_click(0)
        elif Omega_Mouse.first_pop_done == True:
            actions.mouse_click(0)
            actions.mouse_click(0)
            actions.mouse_click(0)
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False

    def omega_mouse_control_click():
        """Control Click then turn off tracking"""
        if Omega_Mouse.first_pop_done == False:
            actions.key("ctrl:down")
            actions.mouse_click(0)
            actions.key("ctrl:up")
        elif Omega_Mouse.first_pop_done == True:
            actions.key("ctrl:down")
            actions.mouse_click(0)
            actions.key("ctrl:up")
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False

    def omega_mouse_shift_click():
        """Shift Click then turn off tracking"""
        if Omega_Mouse.first_pop_done == False:
            actions.key("shift:down")
            actions.mouse_click(0)
            actions.key("shift:up")
        elif Omega_Mouse.first_pop_done == True:
            actions.key("shift:down")
            actions.mouse_click(0)
            actions.key("shift:up")
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            Omega_Mouse.first_pop_done = False
    
    def omega_mouse_relocate():
        """Moves cursor if first pop was already activated in 2-phase process"""
        gaze_window = Omega_Mouse.setting_gaze_capture_interval.get()
        head_lag = Omega_Mouse.setting_head_track_lag.get()
        if Omega_Mouse.first_pop_done == False:
            pass
        elif Omega_Mouse.first_pop_done == True:
            actions.tracking.control_head_toggle(False)
            actions.tracking.control_gaze_toggle(True)
            actions.sleep(gaze_window)
            actions.tracking.control_gaze_toggle(False)
            actions.sleep(head_lag)
            actions.tracking.control_head_toggle(True)
            Omega_Mouse.first_pop_done = True
    
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
    
