from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from PongBall import *
from PongPaddle import *
from Game import *

class PongGameServer(Game):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def __init__(self):
        Game.__init__(self)
        self.ball = PongBall()
        Clock.schedule_interval(PongGameServer.update, 1.0 / 60.0)
    
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        
    def resetBall(self):
        self.pos = self.center
    
    def serve_ball(self, vel=(4, 0)):
        self.ball.velocity = vel
    
    def update(self):
        self.ball.move()
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
    