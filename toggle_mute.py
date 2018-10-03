#!/usr/bin/python3
from pulsectl import Pulse
from dynmen.rofi import Rofi
from dynmen.menu import MenuError
import notify2 as pynotify

pynotify.init("Vol notify")
PULSE = Pulse()
NOTE = pynotify.Notification("Volume", "0", "/usr/share/icons/Faenza/apps/48/"
                                                  "gnome-volume-control.png")
NOTE.set_urgency(0)

def get_sinks():
    """
    Get a list of active pulseaudio sinks
    :return: List. A list containing all the active sink objects.
    """

    # Get the list of input sinks
    sinks = [sink for sink in PULSE.sink_input_list()
             if sink.proplist.get("application.process.binary", None) is not None]

    # Return the list of active sinks
    return sinks


def toggle_mute_sinks(sinks):
    """
    Simply toggle the mute status of all given sinks.
    :param sinks: A list of sink objects.
    :return: Nothing.
    """

    # Toggle the mute status
    for sink in sinks:
        muted = bool(sink.mute)
        PULSE.mute(sink, mute=not muted)


if __name__ == "__main__":
    # Get the list of active sinks
    sinks = get_sinks()
    # Get the names of the apps linked to the sinks
    app_sinks = {"{} {}".format(sink.proplist.get("application.name"), sink.index): sink for sink in sinks}
    if len(app_sinks) > 1:
        # Display a menu to select the application to control
        menu = Rofi()
        menu.hide_scrollbar = True
        menu.prompt = "App. name?"
        try:
            res = menu(app_sinks)
        except MenuError:
            exit()
        app_sink = res.value
    elif len(app_sinks) == 1:
        _, app_sink = app_sinks.popitem()
    else:
        app_sink = None

    # If successful
    if app_sink is not None:
        # Toggle the mute status of the selected sink
        toggle_mute_sinks([app_sink])

        print(app_sink.mute)
        if app_sink.mute:
            # Declare a new notification
            NOTE.update("Muted status", "Muted {}".format(app_sink.proplist.get("application.name")), "/usr/share/icons/Faenza/apps/48/gnome-volume-control.png")
        else:
            # Declare a new notification
            NOTE.update("Mute status", "Unmuted {}".format(app_sink.proplist.get("application.name")), "/usr/share/icons/Faenza/apps/48/gnome-volume-control.png")

        # Show the notification
        NOTE.show()
