import sys
from kivy.clock import Clock
from PongPaddle import *
from weakref import WeakKeyDictionary

class Game(object):
    global MIN_PLAYERS
    MIN_PLAYERS = 2
    def  __init__(self):
        self.players = WeakKeyDictionary()
        
    def addPlayer(self, player):
        #player.paddle = PongPadle()
        self.players[player.uuid] = player
        
    def removePlayer(self, player):
        del self.players[player.uuid]
    
    def numberOfPlayers(self):
        return len(self.getPlayers())
    
    def isPlayer(self, player):
        return self.players[player]
    
    def getOpponents(self, player):
        opponents = []
        for p in self.players.items():
            if(p[1].uuid != player.uuid):
                opponents.append(p[1])
        return opponents
    
    def minPlayersConnected(self):
        if self.numberOfPlayers() >= MIN_PLAYERS:
            return True
        else:
            return False
    
    def getPlayers(self):
        allPlayers = []
        for p in self.players.items():
            allPlayers.append(p[1])
        return allPlayers
    
    def update(self):
        raise NotImplementedError("Please Implement this method")
    