import windows

menu_window = windows.Menu()
gameplay_window = windows.Gameplay()
tryagain_window = windows.TryAgain(gameplay_window=gameplay_window)
current_window = menu_window
to_gameplay = False

is_running = True
while is_running:
    is_running = current_window.apply_and_update()

    if menu_window.new_window() or tryagain_window.new_gameplay():
        current_window = gameplay_window

        menu_window.reset()
        
    if gameplay_window.is_over():
        current_window = tryagain_window