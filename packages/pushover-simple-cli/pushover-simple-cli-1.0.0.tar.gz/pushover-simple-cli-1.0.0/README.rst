========
pushover
========

Send quick notifications to pushover from the command line.

A really simple tool for doing so with a minimum of fuss.


* Free software: BSD license
* Set PUSHOVER_API_TOKEN and PUSHOVER_USER_ID in your environment.


Example
-------

You can use pushover to notify yourself of the status of the most recently run command when it finishes::

    make test; pushover -s$? "make test finished!"
