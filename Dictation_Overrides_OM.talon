mode: dictation
tag: user.om_on
-
^omega mouse$: user.omega_mouse_toggle()
^omega restart$: user.omega_mouse_restart()

^(yum | gum)$: user.omega_mouse_left_click()
^(yummer | gummer)$: user.omega_mouse_left_modup_click()
^twill$: user.omega_mouse_double_click()
^trio$: user.omega_mouse_triple_click()
^con$: user.omega_mouse_control_click()
^shill$: user.omega_mouse_shift_click()
^relo$: user.omega_mouse_relocate()
^drag$: user.mouse_drag(0)
^drop$: user.mouse_drag_end()
^omega check state$: user.omega_mouse_state_check()
^wait$: user.omega_mouse_wait()