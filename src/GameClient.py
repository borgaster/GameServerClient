from sys import stdin, exit
import sys
from thread import *
from time import sleep
from PodSixNet.Connection import connection, ConnectionListener


#import pygame
class Player(ConnectionListener):
    
    def __init__(self, host, port, nickName):
        self.Connect((host, port))
        self.playerAttributes = {"dy": 0, "points": 0, "nickName": nickName, "inGame": False, "uuid": None}
        print "Player started"
        print "Ctrl-C to exit"
        # get a nickName from the user before starting
        connection.Send({"action": "nickname", "data": self.playerAttributes})
       
    def Loop(self):
        connection.Pump()
        self.Pump()
    
    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            command = stdin.readline().rstrip("\n")
            #connection.Send({"action":"getClientStatus", "message":self.playerAttributes["uuid"]})
            if(command == 'w'):
                self.playerAttributes["dy"] = self.playerAttributes["dy"] + 1
            elif(command == 's'):
                self.playerAttributes["dy"] = self.playerAttributes["dy"] - 1
            connection.Send({"action":"updatePlayer", "data":self.playerAttributes})
    #######################################
    ### Network event/message callbacks ###
    #######################################
    
    def Network_players(self, data):
        print("*** players: " + ", ".join([p for p in data['players']]))
    
    def Network_message(self, data):
        print(data)
        
    def Network_getUUID(self, data):
        self.playerAttributes["uuid"] = data["message"]
        t = start_new_thread(self.InputLoop, ())
        
    def Network_inGame(self, data):
        self.playerAttributes["inGame"] = data["message"]
        if self.playerAttributes["inGame"] == True:
            print("Game is starting")
        else:
            print("Oponent left game")
        
    # built in stuff

    def Network_connected(self, data):
        print ("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    
    
    