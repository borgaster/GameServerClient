from sys import stdin, exit
import sys
from thread import *
from time import sleep

from GameClient import *
from PodSixNet.Connection import connection, ConnectionListener


if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "host:port"
    print "e.g.", sys.argv[0], "localhost:31425"
else:
    host, port = sys.argv[1].split(":")
    print "Enter nickname: "
    nickname = stdin.readline().rstrip("\n")
    player = Player(host, int(port), nickname)
    while 1:
        player.Loop()
        sleep(0.001)