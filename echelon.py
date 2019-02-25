#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# (C) 2018 J. Nurminen <slinky@iki.fi>
#
# Echelon adds logic to your tmux panes
#

import subprocess
import sys
from pexpect import fdpexpect

tmux_pane = sys.argv[1]

def tmux_display_msg(msg):
    global tmux_pane
    return subprocess.call("tmux display-message -t %s \"%s\"" % (tmux_pane, msg),
            shell=True)

def tmux_send_keys(msg):
    global tmux_pane
    return subprocess.call("tmux send-keys -t %s \"%s\"" % (tmux_pane, msg),
            shell=True)

def prep_string(b):
    if sys.version_info[0] >= 3:
        return b.decode()
    else:
        return b

def send(s):
    # monkeypatch to make send/sendline go to tmux
    global p
    s = p._coerce_send_string(s)
    b = p._encoder.encode(s, final=False)
    return tmux_send_keys(prep_string(b))

print("Starting to listen for pane %s" % tmux_pane)
tmux_display_msg("Started in pane %s" % tmux_pane)

p = fdpexpect.fdspawn(sys.stdin)
# monkeypatch
p.send = send

while 1:
    try:
        # Put your expect script here to react to keywords...
        p.expect("something")
        p.sendline("Hey, you said it")
    except KeyboardInterrupt:
        break

p.close()
print("Bye")
