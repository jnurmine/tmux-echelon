#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# (C) 2019 J. Nurminen <slinky@iki.fi>

# This is your pexpect script.
# It will be run in a loop. Return False to stop iteration, True to continue.
def run(p):
    try:
        p.expect("something")
        p.sendline("\nHey, you said it\n")
    except KeyboardInterrupt:
        return False
    return True

