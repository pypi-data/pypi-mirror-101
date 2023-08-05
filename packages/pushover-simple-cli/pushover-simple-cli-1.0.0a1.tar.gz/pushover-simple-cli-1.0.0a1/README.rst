========
pushover
========

Send quick notifications to pushover


* Free software: BSD license
* Documentation: https://pushover.readthedocs.io.


Example
-------

You can use pushover to notify yourself of the status of the most recently run command when it finishes::

    make test; pushover -s$? "make test finished!"
