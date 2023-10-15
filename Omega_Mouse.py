from talon import Module, Context, actions, ctrl

mod = Module()
mod.tag("om_on", desc="Signals Omega Mouse is toggled on")
mod.tag("omega_full", desc="Signals Full Mode is active")
mod.tag("omega_lite", desc="Signals Lite Mode is active")
mod.tag("omega_basic", desc="Signals Basic Mode is active")

ctx = Context()
ctx_switch = Context()
ctx_switch.matches = """
tag: user.om_on
"""


# ---------- Variables ----------
om_state = False
first_pop_done = False


# ---------- Settings ----------
setting_omega_mouse_mode = mod.setting(
    "omega_mouse_mode",
    type=int,
    default=0,
    desc="Determines which mode of Omega Mouse to use. 0 = Full. 1 = Lite. 2 = Basic"
    )

setting_gaze_capture_interval = mod.setting(
    "gaze_capture_interval",
    type=str,
    default="50ms",
    desc="Sets gaze time window for cursor movement after 'popping noise'/'relo' commands"
    )

setting_head_track_lag = mod.setting(
    "head_track_lag",
    type=str,
    default="50ms",
    desc="Sets interval after gaze tracking before head tracking starts"
    )

# ========== NON-CALLABLE FUNCTIONS ==========
# Releases all modifier keys (Mac users need to replace "alt:up" with "cmd:up")
def omega_mouse_modifiers_release_function():
    actions.key("ctrl:up")
    actions.key("shift:up")
    actions.key("alt:up")
    actions.key("super:up")
    #actions.key("cmd:up")


# ========== CALLABLE FUNCTIONS ==========
@mod.action_class
class OmegaMouseActions:

    def omega_mouse_toggle():
        """Toggles Omega Mouse on/off. When toggling on, checks for mode value."""
        global om_state
        global first_pop_done
        
        if om_state == False:
            om_state = True
            omega_mode = setting_omega_mouse_mode.get()
            if omega_mode == 0:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_zoom_toggle(False)
                first_pop_done = False
                ctx.tags = ["user.om_on", "user.omega_full"]
                print(f"Full mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")
            elif omega_mode == 1:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_zoom_toggle(False)
                ctx.tags = ["user.om_on", "user.omega_lite"]
                print(f"Lite mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")                
            elif omega_mode == 2:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(True)
                actions.tracking.control_zoom_toggle(False)
                ctx.tags = ["user.om_on", "user.omega_basic"]
                print(f"Basic mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")
        else:
            om_state = False
            actions.tracking.control_toggle(False)
            actions.tracking.control_gaze_toggle(True)
            actions.tracking.control_head_toggle(True)
            actions.tracking.control_zoom_toggle(False)
            first_pop_done = False
            ctx.tags = []
            print(f"Omega Mouse off. First pop = {first_pop_done}. tags = {list(ctx.tags)}")
                
    def omega_mouse_restart():
        """Resets Omega Mouse to initial state. Re-checks mode value."""
        global om_state
        global first_pop_done
        
        if om_state == True:
            omega_mode = setting_omega_mouse_mode.get()
            if omega_mode == 0:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_zoom_toggle(False)
                first_pop_done = False
                ctx.tags = ["user.om_on", "user.omega_full"]
                print(f"Full mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")
            elif omega_mode == 1:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
                actions.tracking.control_zoom_toggle(False)
                ctx.tags = ["user.om_on", "user.omega_lite"]
                print(f"Lite mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")                
            elif omega_mode == 2:
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(True)
                actions.tracking.control_zoom_toggle(False)
                ctx.tags = ["user.om_on", "user.omega_basic"]
                print(f"Basic Mode. First pop = {first_pop_done}. tags = {list(ctx.tags)}")                
        else:
            pass
    
    def omega_mouse_left_click():
        """Normal Left Click when Omega Mouse is off"""
        actions.mouse_click(0)
    
    def omega_mouse_left_modup_click():
        """Left Click that releases modifier keys afterwards when Omega Mouse is off"""
        actions.mouse_click(0)
        omega_mouse_modifiers_release_function()
    
    def omega_mouse_double_click():
        """Normal Double Click when Omega Mouse is off"""
        actions.mouse_click(0)
        actions.mouse_click(0)
    
    def omega_mouse_triple_click():
        """Normal Triple Click when Omega Mouse is off"""
        actions.mouse_click(0)
        actions.mouse_click(0)
        actions.mouse_click(0)
    
    def omega_mouse_control_click():
        """Control Click when Omega Mouse is off"""
        actions.key("ctrl:down")
        actions.mouse_click(0)
        actions.key("ctrl:up")

    def omega_mouse_shift_click():
        """Shift Click when Omega Mouse is off"""
        actions.key("shift:down")
        actions.mouse_click(0)
        actions.key("shift:up")

    def omega_mouse_relocate():
        """Does nothing when Omega Mouse is off"""
        print("Does nothing when Omega Mouse is off")
    
    def omega_mouse_wait():
        """Does nothing when Omega Mouse is off"""
        print("Does nothing when Omega Mouse is off")
    
    def omega_mouse_state_check():
        """Checks state of Omega Mouse"""
        gaze_window = setting_gaze_capture_interval.get()
        head_lag = setting_head_track_lag.get()
        print("Omega Mouse states listed below...")
        print("om_state =", om_state)
        print("tags =", list(ctx.tags))
        print(f"gaze window interval = {gaze_window}")
        print(f"head track lag = {head_lag}")
        print("first_pop_done =", first_pop_done)
        print(f"Drag State = {len(ctrl.mouse_buttons_down()) != 0}")
        #print(f" - Left Drag = {0 in list(ctrl.mouse_buttons_down())}")
        #print(f" - Middle Drag = {2 in list(ctrl.mouse_buttons_down())}")
        #print(f" - Right Drag = {1 in list(ctrl.mouse_buttons_down())}")


# ========== OVERRIDDEN FUNCTIONS ==========
@ctx_switch.action_class("user")
class OmegaMouseSwitchOverrides:

    # Turns off Omega Mouse states first before setting Control Mouse to default active state.
    # Helps to insure other eye tracking modes work as intended
    # (with no active remnants from Omega Mouse).
    def control_mouse_switch():
        """Turns off Omega Mouse first before switching to Control Mouse."""
        global om_state
        om_state = False
        actions.tracking.control_toggle(True)
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
        actions.tracking.control_zoom_toggle(False)
        first_pop_done = False
        ctx.tags = []
        print("""Omega Mouse switched to Control Mouse. 'om_state' is now set to False.
              Omega Mouse tags are disabled.""")
    
    # Turns off Omega Mouse and Control Mouse first before setting Zoom Mouse to
    # default active state. Helps to insure other eye tracking modes work as intended
    # (with no active remnants from Omega Mouse).
    def zoom_mouse_switch():
        """Turns off Omega Mouse first before switching to Zoom Mouse."""
        global om_state
        om_state = False
        actions.tracking.control_toggle(False)
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
        actions.tracking.control_zoom_toggle(True)
        first_pop_done = False
        ctx.tags = []
        print("""Omega Mouse switched to Zoom Mouse.'om_state' is now set to False.
              Omega Mouse tags are disabled.""")