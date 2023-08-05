=====
Usage
=====

Pushover is a command line tool which gobbles up every argument and sends them as
a pushover notification message.

One special argument, ``-s``, will be interpreted as the exit code from the last command. If it is `0`,
then a check mark will be prepended to the message, and if it is not zero, a red X will be prepended.

If ``-s`` is not present, no symbol will be added to the message.

Pushover Authentication
-----------------------

You will need an account with the pushover_ service, and you should add your user ID and app token
as envirnment variables in your shell::

    export PUSHOVER_USER_ID=myuserid
    export PUSHOVER_API_TOKEN=myapptoken
