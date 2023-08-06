README
######

Welcome to BOTD,

BOTD is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. You can install it as a service so
it restarts on reboot. It can be used to display RSS feeds, act as a UDP to
IRC relay and you can program your own commands for it.

INSTALL
=======

Installation is through pypi, all commands are as superuser::

 # pip3 install botd 

to run BOTD 24/7 you need to enable the BOTD service under systemd::

 # cp /usr/local/share/botd/botd.service /etc/systemd/system
 # systemctl enable botd
 # systemctl daemon-reload
 # systemctl restart botd

if you don't want botd to startup at boot, remove the service file::

 # rm /etc/systemd/system/botd.service

CONFIGURE
=========

BOTD has it's own CLI, the botctl program. It needs root to lower privileges
to botd user and run a systemd command to run the bot program. You
can run it on the shell prompt and, as default, it won't do anything:: 

 # botctl
 # 

use botctl <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 # botctl cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mod,rem,rss,thr,ver,upt

configuration is done with the cfg command::

 # botctl cfg server=irc.freenode.net channel=\#dunkbots nick=botje
 ok

users need to be added before they can give commands, use the met command::

 # botctl met ~botfather@jsonbot/daddy
 ok

RSS
===

BOTD provides, with the use of feedparser, the possibility to serve rss
feeds in your channel. To add an url use the rss command with an url::

 # botctl rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 # botctl fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 # botctl ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller::

 # botctl krn mods=rss
 ok

UDP
===

BOTD also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
Output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTD, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

COMMANDS
========

Programming your own commands is easy, open /var/lib/botd/mod/hlo.py and add
the following code::

    def hlo(event):
        event.reply("hello %s" % event.origin)

now you can type the "hlo" command, showing hello <user>::

 # botctl hlo
 hello root@console

LICENSE
=======

BOTD is placed in the Public Domain and has no COPYRIGHT and no LICENSE. 

CONTACT
=======

"hf"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
