from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from PodSixNet.Connection import connection, ConnectionListener
from sys import stdin, exit
import sys
import thread


class PongPaddle(Widget):
    score = NumericProperty(0)
    inGame = False
    uuid = None
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget, ConnectionListener):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None) 
    playerAttributes = None
    
    def setupConnection(self, host, port, nickName):
        self.playerAttributes = {"dy": self.player1.pos[1], "score": self.player1.score, 
                            "nickName": nickName, "inGame": False, "uuid": None, "isHost": False, "opponent": None }
        self.Connect((host, port))
        connection.Send({"action": "nickname", "data": self.playerAttributes})
        thread.start_new_thread(self.Loop, ())
        
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        
    def center_ball(self):
        self.ball.center = self.center

    def update(self, dt):
        if (self.playerAttributes["inGame"] == True):
            connection.Send({"action":"getClientStatus", "message":self.playerAttributes["uuid"]})
            if(self.playerAttributes["isHost"] == True):
                self.ball.move()
                #print self.ball.pos
                connection.Send({"action": "updateBall", "data": [self.ball.x, self.ball.y]} )
                #connection.Pump()
            #bounce of paddles
            self.player1.bounce_ball(self.ball)
            self.player2.bounce_ball(self.ball)
    
            #bounce ball off bottom or top
            if (self.ball.y < self.y) or (self.ball.top > self.top):
                self.ball.velocity_y *= -1
    
            #went of to a side to score point?
            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball(vel=(4, 0))
            if self.ball.x > self.width:
                self.player1.score += 1
                self.serve_ball(vel=(-4, 0))
                    
            connection.Send({"action":"updatePlayer", "data":self.playerAttributes})
            connection.Pump()
            self.Pump()
        
    def on_touch_move(self, touch):
        if ((touch.x < self.width / 3)):
            self.player1.center_y = touch.y
        if ((touch.x > self.width - self.width / 3)):
            self.player2.center_y = touch.y
        if (self.playerAttributes["isHost"] == True):
            self.playerAttributes["dy"] = self.player1.pos[1]
        else:
            self.playerAttributes["dy"] = self.player2.pos[1]
        connection.Send({"action":"updatePlayer", "data":self.playerAttributes})
        #connection.Pump()
        #self.Pump()
    
    #######################################
    ### Network event/message callbacks ###
    #######################################
#     def Network(self, data):
#         print("Network!!")
#         #print(data)
    def Network_ballMove(self, data):
        self.ball.x = data["data"][0]
        self.ball.y = data["data"][1]
    
    def Network_isHost(self, data):
        print("Is host")
        self.playerAttributes["isHost"] = data["message"]
        
    def Network_playerStatus(self, data):
        for p in data["message"]:
            #If I am the host, I got the pos of player 2
            if(self.playerAttributes["isHost"] == True):
                print self.player2.pos
                #self.player2.pos[1] = 30#p["dy"]
            #If I am not the host, I got the pos o player 1
            else:
                self.player1.pos[1] = p["dy"]
        
    def Network_getUUID(self, data):
        print "getting UUID",  data["message"]
        self.playerAttributes["uuid"] = data["message"]
        
    def Network_inGameStart(self, data):
        
        self.playerAttributes["opponent"] = data["message"]
        if (self.playerAttributes["opponent"] != None):
            self.playerAttributes["inGame"] = True
            print("Game is starting...")
            Clock.schedule_interval(self.update, 1.0 / 60.0)
            #self.serve_ball()
        else:
            print("Oponent left game")
            self.center_ball()
            self.playerAttributes["inGame"] = False      
        
    # built in stuff

    def Network_connected(self, data):
        print ("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()
        
    def Loop(self):
        while True:
            connection.Pump()
            self.Pump()


class PongApp(App):
    def build(self):
        #nickname = stdin.readline().rstrip("\n")
        game = PongGame()
        game.setupConnection("localhost", 12345, "nickname")
        #game.serve_ball()
        return game


if __name__ == '__main__':
    PongApp().run()