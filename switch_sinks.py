#!/usr/bin/python3
from pulsectl import Pulse
from dynmen.rofi import Rofi
from dynmen.menu import MenuError

# Instantiate the interface to the PulseAudio server
p = Pulse()

# List the available sink inputs
sink_ins = {"{} {}".format(s.proplist.get("application.name"), s.index):s.index for s in p.sink_input_list()}
# List the available sinks
sinks = {s.description:s.index for s in p.sink_list()}

# Initialize the menu displayed to the user
menu = Rofi()
menu.hide_scrollbar = True
menu.prompt = "Sink?"

# Ask the user to choose
try:
    # The sink input
    if len(sink_ins) == 1:
        _, s_in_idx = sink_ins.popitem()
    elif len(sink_ins) > 1:
        s_in_idx = menu(sink_ins).value
    else:
        exit(0)

    # The sink to move the input to
    if len(sinks) > 0:
        s_idx = menu(sinks).value
    else:
        exit(0)
except MenuError:
    exit(-1)

# Move the sink input to the chosen sink
if s_in_idx is not None and s_idx is not None:
    p.sink_input_move(s_in_idx, s_idx)
