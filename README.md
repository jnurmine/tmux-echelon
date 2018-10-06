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

Remember to:

```
chmod 755 echelon-wrapper.sh
chmod 755 echelon.py
```

Next, prepare your tmux windows and panes.

Then, to start things up, issue this tmux command (by pressing the attention
key, and don't forget the colon):

```
:pipe-pane "exec ~/bin/echelon-wrapper.sh #D"
```

Note: Here the #D refers to the current pane. If you want the output to go to a
different pane, you need to give the pane-id of that pane. You can check the
current pane-id with:

```
:display-message "#D"
```

If you did not change the script, try typing "something" and hit enter.

To turn it off:

```
:pipe-pane
```

## Customization

See the echelon.py for comments. The (p)expect logic goes inside the while 1
block.

You may need to disable the timeout with `p.expect("foobar", timeout=None)`.
See [pexpect documentation](https://pexpect.readthedocs.io/) for more details.

## TROUBLESHOOTING 

If it does not seem to work:

  * Try a newer tmux
  * If you upgrade, kill existing tmuxes (otherwise the old one will be used
    through the default server socket)
