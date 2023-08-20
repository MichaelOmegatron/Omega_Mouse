# ----- Omega Mouse Mode Selection -----
settings():
	# Set which Omega Mouse mode to use. Omega Mouse restart required with change.
	# 0 = Full
	# 1 = Lite
	# 2 = Basic
	user.omega_mouse_mode = 0



# ----- Omega Mouse Toggle Switching -----
omega mouse: user.omega_mouse_toggle()
omega restart: user.omega_mouse_restart()
#control mouse: {uses Omega Mouse function placed into mouse.talon. See "Set-Up" in readme.}
#zoom mouse: {uses Omega Mouse function placed into mouse.talon. See "Set-Up" in readme.}



# ----- Omega Mouse Features -----
#*Popping Noise*: {overrides default pop click for Omega Mouse functionality}
(yum | gum): user.omega_mouse_left_click()
(yummer | gummer): user.omega_mouse_left_modup_click()
twill: user.omega_mouse_double_click()
relo: user.omega_mouse_relocate()
#drag: {overrides default mouse_drag in mouse.py for Omega Mouse functionality}
drop: user.mouse_drag_end()
#(drag end | end drag | drop): {overrides default mouse_drag_end in mouse.py for Omega Mouse functionality}
omega check state: user.omega_mouse_state_check()
wait: user.omega_mouse_wait()