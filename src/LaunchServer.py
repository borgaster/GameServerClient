from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from GameServer import *

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = GameServer(localaddr=(host, int(port)))
    s.Launch()