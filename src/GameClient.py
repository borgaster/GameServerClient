from sys import stdin, exit
import sys
from thread import *
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener


#import pygame
class Player(ConnectionListener):
    
    def __init__(self, host, port, nickName):
        self.nickName = nickName
        self.points = 0
        self.dy = 0
        self.Connect((host, port))
        self.inGame = False
        print "Player started"
        print "Ctrl-C to exit"
        # get a nickName from the user before starting
        
        connection.Send({"action": "nickName", "nickName": self.nickName})
        # launch our threaded input loop
        t = start_new_thread(self.InputLoop, ())
                
            
    
    def Loop(self):
        connection.Pump()
        self.Pump()
    
    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
        #    connection.Send({"action": "message", "message": self.__dict__})
            command = stdin.readline().rstrip("\n")
        #    if(command == 'w'):
        #        self.dy = self.dy + 1
        #    elif(command == 's'):
        #        self.dy = self.dy - 1
        #    print self.__dict__
            
    
    #######################################
    ### Network event/message callbacks ###
    #######################################
    
    def Network_players(self, data):
        print "*** players: " + ", ".join([p for p in data['players']])
    
    def Network_message(self, data):
        print data
    def Network_inGame(self, data):
        self.inGame = data["message"]
        if self.inGame == True:
            print "Game is starting"
        else:
            print "Oponent left game"
        
    # built in stuff

    def Network_connected(self, data):
        print "You are now connected to the server"
    
    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
    
    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()

    
    
    