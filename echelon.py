#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# (C) 2018 J. Nurminen <slinky@iki.fi>
#
# Echelon adds logic to your tmux panes
#

import subprocess
import sys
from pexpect import fdpexpect

class TmuxInfo:
    def __init__(self, session=None, window=None, pane=None):
        self.session = session
        self.window = window
        self.pane = pane

    def __str__(self):
        return "%s:%s.%s" % (self.session, self.window, self.pane)

def shell_safe_quote(msg):
    # bash will mess up special chars, prevent this
    msg = msg.replace("%", "%%")
    return msg.replace("'", "'\"'\"'")

def tmux_display_msg(msg):
    global tmux_info
    return subprocess.call("tmux display-message -t '%s' '%s'" %
            (tmux_info, shell_safe_quote(msg)), shell=True)

def tmux_send_keys(msg):
    global tmux_info
    return subprocess.call("tmux send-keys -t '%s' \"%s\"" %
            (tmux_info, msg), shell=True)

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

tmux_info = TmuxInfo(
        session = sys.argv[1],
        window = sys.argv[2],
        pane = sys.argv[3])

s = "Listening in this pane. Target: session: %s, window: %s, pane: %s (%s)" % \
        (tmux_info.session, tmux_info.window, tmux_info.pane, tmux_info)

print(s)
tmux_display_msg(s)

p = fdpexpect.fdspawn(sys.stdin)
# monkeypatch
p.send = send

while 1:
    try:
        # Put your expect script here to react to keywords...
        p.expect("something")
        p.sendline("\nHey, you said it\n")
    except KeyboardInterrupt:
        break

p.close()
print("Bye")
