import sys
from weakref import WeakKeyDictionary


class Game():
    global MIN_PLAYERS
    MIN_PLAYERS = 2
    def  __init__(self):
        self.players = WeakKeyDictionary()
    
    def addPlayer(self, player):
        self.players[player] = player
        
    def removePlayer(self, player):
        del self.players[player]
    
    def numberOfPlayers(self):
        return len(self.getPlayers())
    
    def isPlayer(self, player):
        return self.players[player]
    
    def minPlayersConnected(self):
        if self.numberOfPlayers() >= MIN_PLAYERS:
            return True
        else:
            return False
    
    def getPlayers(self):
        allPlayers = []
        for p in self.players:
            allPlayers.append(p)
        return allPlayers
    