=============
Git annex gui
=============
A small systray app for git annex assistant. The documentation below assumes a
centralized setup with a self-hosted server as described here:

https://git-annex.branchable.com/tips/centralized_git_repository_tutorial/on_your_own_server/

Installation
============

Install from pypi::

    $ pip install --user git-annex-gui

Install from gitlab::

    $ git clone
    $ mkvirtualenv git-annex-gui
    $ pip install -e .

Setup and configuration
=======================

Ssh configuration
-----------------

Create ssh keys. Use default file path or type in. Type in pass phrase::

    $ ssh-keygen
    
Add key to `ssh-agent`. If not default file path used, type in path::

    $ ssh-add
    
Copy public key to remote git annex server::

    $ ssh-copy-id user@gitannex.domain.org


Connect to central repo
-----------------------
Connecting to a central repo is more or less equivalent to whats described under
the "make a checkout" section here:

https://git-annex.branchable.com/tips/centralized_git_repository_tutorial/on_your_own_server/

The relevant instructions::

    $ git clone ssh://user@gitannex.domain.org/~/annex
    $ cd annex
    $ git annex init

`git-annex-gui` also assumes there is a `~/.config/git-annex/autostart` file
listing the repos to be handled by git-annex assistant. For instance, containing
something like::

    /home/<user>/annex    

With this in place, git-annex-gui can be started::

    $ git-annex-gui

An icon should appear in the systray. Right the icon, choose start and the
assistants' web page should appear in its own window, where eventually
information about sync activities should be shown.

One could possibly also get the appropriate sync setup by running the git-annex
assistant and completing the setup wizard there.

ROADMAP
=======

v0.4 - basic features
---------------------
- [ ] Implement open annex dir in file explorer. Use `xdg-open`?
  - What about BeOS style file navigation in the systray sub-menu?
- [ ] Implement start of app when desktop starts.
- [ ] Implement starting of annex daemon when app starts.

v0.5 - desktop integration
--------------------------
- [ ] Forward notifications to desktop notification system?

v0.6 - in-app documentation/assistant
-------------------------------------
- [ ] add in-app documentation to aid in

  - [ ] starting the assistant wizard
  - [ ] setting remote central repo
- [ ] see what else of existing documentatio can be used in-app

Development
===========
To setup for development, run::

    $ pip install -e .[dev]

Otherwise, this project use `sykel` for release handling etc:
https://pypi.org/project/sykel/

Resources
=========

REST interface
--------------
Check the routes file in the git-annex repo (under assistant/webapp) to get an
understanding about the REST interface.

Misc
----
- recovery from corrupt repo: http://git-annex.branchable.com/tips/recovering_from_a_corrupt_git_repository/
- how to setup central repo setup
