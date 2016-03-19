import uuid
from PodSixNet.Channel import Channel

class PlayerServer(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickName = "anonymous"
        self.inGame = False
        self.game = None
        self.gameClient = None
        self.uuid = uuid.uuid1()
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_updateBall(self, data):
        playersInGame = self.game.getPlayers()
        for p in playersInGame:
            p.Send({"action": "ballMove", "data": data["data"]})
    
    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickName})
        
    def Network_nickname(self, data):
        self.gameClient = data["data"]
        self.nickName = self.gameClient["nickName"]
        print self.nickName, " entered the game"
        #self._server.SendPlayers(self.nickName)
    
    def Network_updatePlayer(self, data):
        self.gameClient = data["data"]
        
    def Network_getClientStatus(self, requestorUUID):
#        print "Get client status ", requestorUUID
        player = self._server.getPlayer(requestorUUID)
        opponents = player.game.getOpponents(player)
        playerStatuses = []
        for p in opponents:
            playerStatuses.append(p.gameClient)
        data = {"action": "playerStatus", "message": playerStatuses}
        self._server.sendPlayer(requestorUUID, data)
        
        