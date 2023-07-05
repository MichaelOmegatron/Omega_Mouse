from talon import Module, Context, noise, actions

mod = Module()
# Creates tag for when Omega Mouse state is On
mod.tag("om_on", desc="Signals Omega Mouse is toggled on")

#def on_pop(active):
#    print("pop")
#noise.register("pop", on_pop)

# NOTE: Every user defined tag needs to be prefixed with user. , so mm_on becomes user.mm_on and so on.
# Only talon defined tags like browser can be used without a user. prefix.
# Context for Omega Mouse commands
ctx = Context()
ctx_om_on = Context()
ctx_om_on.matches = """
tag: user.om_on
"""

# Define a variable to control noise_pop phase
first_pop_done = False

om_state = False

# Limit Omega Mouse toggle to only when omega_mouse_permission exists. Real function.
# When Omega Mouse toggles on, Gaze and Head tracking are set off. When Omega Mouse
# toggles off, Gaze and Head tracking are set to on.
def omega_mouse_toggle_function():
    global om_state
    if actions.tracking.control_enabled() == True:
        if om_state == False:
            om_state = True
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)
            ctx.tags = ["user.om_on"]
            print("om_state is now set to True. user.om_on tag is enabled")
        else:
            om_state = False
            actions.tracking.control_gaze_toggle(True)
            actions.tracking.control_head_toggle(True)
            ctx.tags = []
            print("om_state is now set to False. user.om_on tag has been disabled")
    else:
        print("Function only available when Control Mouse is active")
        om_state = False

@mod.action_class
class Actions:

    def omega_mouse_toggle():
        """Toggle the Omega Mouse functionality, but only if the control mouse is enabled"""
        omega_mouse_toggle_function()

# Phase 1: Pop sound enables gaze control briefly to move cursor > gaze control disables >
#          Head tracking enables > removes before tag > Enables tag for second click.
# Phase 2: Pop sound left clicks > turns off head tracking > removes after tag >
#          Enables tag for first click.
@ctx_om_on.action_class("user")
class OmegaMouseActions:

    def noise_trigger_pop():
        """First pop toggles head tracking, second pop confirms click"""
        global first_pop_done
        if first_pop_done == False:
            """Move cursor to gaze then switch to head tracking"""
            actions.tracking.control_gaze_toggle(True)
            actions.sleep("50ms")
            actions.tracking.control_gaze_toggle(False)
            actions.sleep("50ms")
            actions.tracking.control_head_toggle(True)
            first_pop_done = True
        elif first_pop_done == True:
            """Left click and disable head tracking"""
            actions.mouse_click(0)
            actions.tracking.control_head_toggle(False)
            first_pop_done = False


# While OM is active, command "control mouse" should reactivate gaze and head tracking, and switch 
# controll mouse off.
#   def control_mouse_toggle()
#       actions.tracking.control_mouse(False)
#       actions.tracking.control_gaze_toggle(True)
#       actions.tracking.control_head_toggle(True)
#
#

# Still need to add context for control mouse while Omega Mouse is active so that
# gaze and head control both turn back on after I say "control mouse" to close it.
# I just want the command "control mouse" to also set gaze and head control to on.

# Why does omega_mouse_toggle need to exist seperately to house omega_mouse_toggle_function?
# Can we skip the middle man? Why do i need to call the prior to get to the later?
# Can i just call the later directly?