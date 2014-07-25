***********************************************
sylloge of codes documentation and instructions
***********************************************

Thanks for showing my piece *sylloge of codes*! I wanted to provide some info regarding the piece and how to manage it. It's important to read through all of the instructions below to understand how the piece functions and what needs to happen each day. Thanks for your understanding!

Parts
=====

The piece consists of the box, and a Raspberry Pi computer running Debian Linux and pico projector inside. On the Raspberry Pi is custom software that I have written. Also, there are two wireless modules attached to the Pi (one is currently unused). The wireless module creates a local wireless network that visitors to the piece can connect to. This module is not connected to the internet, and thus does not allow visitors any external internet access.

Running
=======

The piece is designed to run fairly autonomously, and hopefully little interaction will be necessary, with the exception of curation (see :ref:`curation-ref`). However, I did want to provide you with some information in case something goes wrong. You can always contact me as well: :ref:`contact-ref` 

Admin
-----

There is an admin section of the website. To access, connect to the ``sylloge_of_codes`` wireless network and type in ``sylloge.of.codes`` in your browser. In the footer of the page will be a link that says ``Admin``. Click the link and you'll be taken to a place where you can enter in admin username  (``admin``) and password (``adm1nsyll0g3``). You'll be taken to a page with two main links, ``Curation`` and ``Shutdown``. See below for more info.

.. _curation-ref:

Curation
--------

Given that this is a piece that asks people to contribute their own codes, it seemed prudent to enable some form of moderation. The ``Curation`` area allows you to do that.

.. note::

    The Raspberry Pi is very powerful for its size, but it's still rather slow. The ``Curation`` page will take a while to load. Please be patient!

The page is ordered by most recent contributions first. Tick the checkbox before those that you want to be enabled and click submit (remember the Pi is somewhat slow, so be patient!). The changes will take place immediately. 

.. note::

    The projection software chooses randomly from the enabled contributions, so it might take a while for you to see newly enabled contributions.

General hookup
--------------

Plugin the projector. To turn on the projector, use the included remote. You shouldn't need to change settings on the projector itself (the most important is the color setting, third item down on the Menu; it should be on "Cinema Mode"). The HDMI cable should connect to the Pi. You can focus the projector using the movable tab on the top left.

The Pi should sit on the top right. You connect the Micro-USB cable to the Pi (the cable can go underneath the HDMI cable) and then to the outlet. The Pi will boot automatically.


Daily Startup and Shutdown
--------------------------

The piece should be shutdown at night and started up again in the morning.

Startup
^^^^^^^

The installation is set to start automatically on boot. After the Linux boot messages will come three stages. The first is called "process pdfs". This creates PDFs of recently contributed codes. One PDF (from those codes that are "enabled") is randomly selected and presented to the contributor after submission. This process can take quite a while, so please be patient.

The second step is "start uwsgi". This starts up the embedded web server.

.. note::
    This takes a while (5 minutes), as the web server needs a while to process all of the files and translations. Please be patient.

The third and final step is "start sylloge of codes OF". This starts the graphical projection.

Shutdown
^^^^^^^^

The piece should be shutdown in the evening, so that in the morning the "process pdfs" step can be run. To do so, login to the ``Admin`` section of the website. There is a ``Shutdown`` link. Click it, and the Pi will shutdown. Use the remote to turn off the projector. Turn off the powerstrip that holds both the projector and the Pi.

To reiterate
^^^^^^^^^^^^

In the morning, turn on the powerstrip to restart the Pi. In the evening, login as ``admin``, click ``Shutdown``, wait for the Pi to shutdown, shut off the projector, and turn off the powerstrip.

Login
-----

You are unlikely to need to login remotely.  However, you can login to the machine in a couple of different ways. The preferred way involves you connecting to the "sylloge_of_codes" wireless network and using SSH to login (use PuTTY on Windows or Terminal on Mac OSX). The IP address for the Pi is 10.1.0.1. The username is ``pi`` and the password is ``n3wc0d3s``. Alternatively, you can take parts of the box apart, attach a USB keyboard to the Raspberry Pi inside, reboot, wait for the software to complete loading, and hit escape. You'll be dropped to a command-prompt.

Beware that the ``pi`` account has full root access via ``sudo``! So be careful with any commands that you might type in.


.. _contact-ref:

Contact
=======

Please don't hesitate to contact me with any questions!

E-mail: nknouf@wellesley.edu or nknouf@zeitkunst.org

Phone: +1 617 388 0567

Skype: nickknouf

