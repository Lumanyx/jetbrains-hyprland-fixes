import json
import subprocess
from time import sleep

#
# Simple Python script for fixing distorted menus (e.g. Go to file (Ctrl + N)) on Hyprland.
# For some reason, some dialogs on JetBrains IDEs fail to resize properly(?) which causes
# them to become stretched. I cannot say for certain if this is JetBrains' or Hyprland's fault,
# but it was so annoying that I just ended up writing this script.
#
# The workaround consists of resizing dialogs slightly when they're opened.
# While this does solve the visual distortion, cursor/mouse detection seems to still be wrong.
# As long as you're only using the "Go to file" dialog with your keyboard, it should still be fine.
#
class ActiveWindow:
    def __init__(self, address):
        self.address = address

def get_active_window():
    # Retrieve active window data from hyprctl
    data = subprocess.check_output(["hyprctl", "activewindow", "-j"])
    parsed = json.loads(data.decode("utf-8"))

    if 'class' not in parsed:
        return None
    # Ignore if no class is present
    if parsed["class"] is None:
        return None
    # Only target windows of JetBrains IDEs
    if not str(parsed["class"]).startswith("jetbrains-"):
        return None
    # The IDE window we're looking for has no title
    if not len(str(parsed["title"])) == 0:
        return None

    return ActiveWindow(parsed["address"])

# Hacky workaround to force the window to redraw by slightly resizing it
def redraw_window():
    print("Forcing window redraw...")
    subprocess.check_output(["hyprctl","dispatch", "resizeactive", "1%", "1%"])

def watch_windows():
    # Use a breakpoint in the code line below to debug your script.
    lastAddress = ""
    while True:
        sleep(0.2)
        data = get_active_window()

        if data is None:
            # Reset if the target window is not open rn
            lastAddress = ""
            continue

        if data.address != lastAddress:
            lastAddress = data.address
            redraw_window()


if __name__ == '__main__':
    watch_windows()
