Theatre of Spud
:::::::::::::::

February 14th, 1984.

Somewhere in the English Midlands, a humble local side will for the second time battle mighty Liverpool
in the football cup tie of a lifetime.

And across town on this cold foggy night, Edward Lionheart debuts his youth production of `Arms and the Man`.

Amid technical hitches, one withering critic and a diabolical director, can a young boy called *Spud*
save this theatre from disaster?

Status
++++++

This project is in early alpha. It lacks some content and it's slightly buggy.
It was submitted as a demo to `Spring Thing 2021`_.

Installation
++++++++++++

* Windows_
* Linux_

Windows
=======

`Theatre of Spud` is a command line program.
You use it from the Windows command interpreter.

To launch a new command window:

#. Tap the Windows key so that the Start Menu pops up.
#. Type the word `cmd`.
#. When you see the *Command Prompt* app highlighted, tap the Enter key.

You should see a prompt like this (your user name will differ)::

    Microsoft Windows [Version 10.0.18362.1139]
    (c) 2019 Microsoft Corporation. All rights reserved.

    C:\Users\author>

Prerequisites
-------------

Download and install Python from https://www.python.org/ . You need Python version 3.9 or higher.
Make sure to check the option to add `python` to your environment path.
This makes command line operation more easy.

After you've installed Python, open a command window and type `python`.
You should see something like this::

    C:\Users\author>python
    Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Type `quit()` and press Return.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python -m venv C:\Users\author\catchphrase-app

#. Update the package manager within it::

    C:\Users\author\catchphrase-app\Scripts\pip install -U pip wheel

Download
--------

#. Download the `repository as a zip file <https://github.com/tundish/theatre_of_spud/archive/master.zip>`_.
   Unzip it to a local directory.

#. `cd` to `theatre_of_spud`.

Install
-------

#. Install `Theatre of Spud` and dependencies::

    C:\Users\author\catchphrase-app\Scripts\pip install .

Run
---

You can run the demo in two modes.

#. Text-only in the terminal::

    C:\Users\author\catchphrase-app\Scripts\python -m tos.main

#. Launch a local web server to play the web app (`http://localhost:8080`)::

    C:\Users\author\catchphrase-app\Scripts\python -m tos.app

Linux
=====

The Linux command line is generally more easy to work with than the Windows command prompt.
If you're finding the Windows command prompt tricky, you can install `Git Bash`_ which behaves in a
Linux-like way.

I encourage you to move to a Linux operating system when you are able. 
You can try one out at little cost on a `Raspberry Pi`_ or similar device.

Here are the install instructions for Linux. You need Python version 3.9 or higher.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python3 -m venv ~/catchphrase-app

#. Update the package manager within it::

    ~/catchphrase-app/bin/pip install -U pip wheel

Download
--------

#. Download the `repository as a zip file <https://github.com/tundish/theatre_of_spud/archive/master.zip>`_.
   Unzip it to a local directory.

#. `cd` to `theatre_of_spud`.

Install
-------

#. Install `Theatre of Spud` and dependencies::

    ~/catchphrase-app/bin/pip install .

Run
---

You can run the demo in two modes.

#. Text-only in the terminal::

    ~/catchphrase-app/bin/python -m tos.main

#. Launch a local web server to play the web app (`http://localhost:8080`)::

    ~/catchphrase-app/bin/python -m tos.app


The freedom to copy
+++++++++++++++++++

You are free to use this project as a teaching example, or as the basis of your own work.
Please read the licence and make sure you `understand the Affero GPL`_.

.. _Git Bash: https://gitforwindows.org/
.. _Raspberry Pi: https://www.raspberrypi.org/
.. _understand the Affero GPL: https://www.gnu.org/licenses/why-affero-gpl.html
.. _Spring Thing 2021: https://www.springthing.net/2021/

