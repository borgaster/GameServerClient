from PodSixNet.Channel import Channel
class PlayerServer(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickName = "anonymous"
        self.inGame = False
        self.game = None
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickName})
        
    def Network_nickname(self, data):
        self.nickName = data["nickName"]
        print self.nickName, " entered the game"
        self._server.SendPlayers(self.nickName)