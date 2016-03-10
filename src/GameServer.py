import sys
from time import sleep, localtime
import uuid
from weakref import WeakKeyDictionary
from Game import *
from PlayerServer import *
from PongGameServer import *
from PodSixNet.Server import Server

class GameServer(Server):
    channelClass = PlayerServer
    def __init__(self, *args, **kwargs):
        self.players = WeakKeyDictionary()
        self.games = WeakKeyDictionary()
        self.other = None
        Server.__init__(self, *args, **kwargs)
        print 'Server launched'
        
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
        

    def AddPlayer(self, player):
        print "Adding player "
        game = self.getAvailableGames()
        uuid = player.uuid
        self.players[uuid] = player
        player.Send({"action":"getUUID", "message": str(uuid)})
        if not game is None:
            player.inGame = True
            self.games[game].addPlayer(player)
            player.game = game
            opponents = game.getOpponents(player)
            if (game.minPlayersConnected() == True):
                player.inGame = True
                #player.Send({"action": "inGameStart", "message": str(opponents[0].uuid)})
                #self.other.Send({"action":"inGameStart", "message": str(uuid)})
                for p in opponents:
                    p.Send({"action":"inGameStart", "message": str(uuid)})
                    self.players[p.uuid].inGame = True       
        else:
            game = Game()
            game.addPlayer(player)
            self.games[game] = game
            player.game = game
            player.Send({"action": "isHost", "message": True})   
            self.other = player
            
    def getAvailableGames(self):
        game = None
        listGames = self.games.values()
        for g in listGames:
            if g.numberOfPlayers() == 1:
                game = g
                break
        return game
    
    def getPlayer(self, playerUUID):
        uuid = self.convertUUID(playerUUID)
        return self.players[uuid]
    
    def DelPlayer(self, player):
        print "Deleting Player " + str(player.nickName)
        game = player.game
        game.removePlayer(player)
        players = game.getPlayers()
        if game.minPlayersConnected() == False:
            if len(players) >= 1:
                [p.Send({"action": "message", "message": "Not enough players"}) for p in players]
                [p.Send({"action":"inGameStart", "message": None}) for p in players]
            else:
                del self.games[game]
        else:
            [p.Send({"action": "message", "message": str(p.nickName) + " left the game"}) for p in players]
            
    def sendPlayer(self, playerUUID, data):
        uuid = self.convertUUID(playerUUID)
        self.players[uuid].Send(data)
        
    def SendPlayers(self, nickName):
        self.SendToAll({"action": "message", "message": str(nickName) + " has joined"})
    
    def convertUUID(self, data):
        strUUID = uuid.UUID(data["message"]).hex
        return uuid.UUID(strUUID)
    
    def SendToAll(self, data):
        print self.players
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


    