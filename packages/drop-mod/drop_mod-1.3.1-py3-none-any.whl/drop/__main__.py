# the user wants to run drop directly
import os

run_gui = True

# check if it'll be possible to run drop-gui
if (os.getenv("DISPLAY") is None) and (os.name == 'posix'):
    run_gui = "Cannot run drop-gui due to no DISPLAY variable: this likely means that this session is running " \
              "without graphics interface, such as in a tty terminal."
# i have no idea how this will work for Windows. can you even not run have a UI on Windows? is that even possible?
try:
    from dearpygui.core import *
    from dearpygui.simple import *
except ImportError:
    run_gui = "Dear PyGui not installed, no way of running the GUI without the core GUI library."

if type(run_gui) is not str:
    import drop.gui
    drop.gui.start_gui()
else:
    exit(run_gui)
