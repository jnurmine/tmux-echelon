# tmux-echelon

Expect handling for a tmux pane (Python scripted)

## What is this?

Basically, you can automate things.

This tool lets you feed a tmux pane through a (p)expect script, reacting to the
input by sending output back to the pane (or another pane). The logic can be as
complex as you like, as the script runs locally in your machine.

The target device does not need to have expect, pexpect or any scripting
environment.

## Give me an example / I need inspiration

To be more concrete, here are some examples.

Suppose you are developing on an embedded device. There's a serial connection
and no scripting environment:

  * You don't want to persist development-time bootloader
  settings in U-boot. You want to netboot instead of flash boot, and also have
  other customizations which intercept the normal startup, replacing those with
  your special things.

Or, suppose you are building new software on a build machine and you want to
auto-deploy it to the previously mentioned embedded device:

  * When the build is finally done, you want to automate deployment to your
  test devices, and start these up. As part of the build process, you copy the
  resulting files to the tftp directory, then send commands to *another pane*
  (which has the serial connection) to reboot the board. See below how to do this.

## How do I use it?

The instructions assume you have a ~/bin and want to put things there. If you
use another path, edit the echelon-wrapper.sh.

First, you need to be able to run pexpect with Python. The cleanest way to setup
this is using a virtualenv:

```
cd ~/bin
virtualenv -p python echelon-py
. echelon-py/bin/activate
pip install pexpect
```

You can exit that shell.

You can use either Python 2.7 or Python 3.x.

Remember to:

```
chmod 755 echelon-wrapper.sh
chmod 755 echelon.py
```

Next, prepare your tmux windows and panes.

Then, to start things up, issue this tmux command (by pressing the attention
key, and don't forget the colon):

```
:pipe-pane "exec ~/bin/echelon-wrapper.sh '#{session_id}' #{window_id} #{pane_id}"
```
Note: single quotes MUST be used around session_id.

If you did not change the script, try typing "something" and hit enter.

To turn it off:

```
:pipe-pane
```

Note: If you want the output to go to a different session, and/or window,
and/or pane, you need to give the pane-id of that pane. You can check the
required parameters with:

```
:display-message "#{session_id} #{window_id} #{pane_id}"
```

Because of tmux internals, the session id always starts with a dollar sign ($).
The window id has an "at" (@) and the pane id has a percentage symbol (%).

The used server socket is always the default server called "default". Using a
different server is currently not supported.

If you don't like numeric ids, you can rename some of them. Please see the tmux
documentation for details (rename-session, rename-window).

## Tmux key binding

Tip: to be more effective, bind a key in tmux. Use this in ~/.tmux.conf:

```
bind-key J pipe-pane "exec ~/bin/echelon-wrapper.sh '#{session_id}' #{window_id} #{pane_id}"
bind-key j pipe-pane
```

Then attention key + J will turn on tmux-echelon, and attention key + j will disable it.

## Logging the session

To keep a record of the whole session, you can enable logging.
Simply set the environment variable ECHELON_LOG when invoking exec:

```
bind-key J pipe-pane "ECHELON_LOG=/tmp/tmux-echelon-#W.log exec ~/bin/echelon-wrapper.sh '#{session_id}' #{window_id} #{pane_id}"
bind-key j pipe-pane
```

The #W is replaced with the pane name. For example, in the above case, if you
have a pane called "my-cool-robot", the log file would be "/tmp/tmux-echelon-my-cool-robot.log".

## Debugging your script

Start the script from command line.

Let's say session_id is $3, window_id is @1 and pane_id is %3:

```
~/bin/echelon-wrapper.sh '$3' @1 %3
```

You need to quote the session_id, otherwise the shell interprets it.
For example, session_id 0 would become $0 and thus the name of your shell (/bin/bash).

## Customization

See the echelon.py for general plumbing and comments.

Put your script into script.py; the (p)expect logic is in a function called
"run". The pexpect instance is given as a parameter. Return True if you want to
continue iteration and False to stop.

You may need to disable the timeout with `p.expect("foobar", timeout=None)`.
See [pexpect documentation](https://pexpect.readthedocs.io/) for more details.

## TROUBLESHOOTING 

If it does not seem to work:

  * Try a newer tmux
  * If you upgrade, kill existing tmuxes (otherwise the old one will be used
    through the default server socket)

If you've changed the echelon.py:

  * The shell quoting is nasty and brittle. Try to run directly from command
    line first. If this works, the problem is likely some quoting issue, such as
    the dollar sign in the session.

To debug your own script.py:

  * In general, test by running directly from the command line first.
