import pygame
import random
import rospy
import math
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

rospy.init_node('Remote', anonymous=True)

current_pos = PoseStamped()

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    x_curser1 = 320
    y_curser1 = 240

    mode= ''
    count = 0
    radius = 10
    screen.fill((0, 0, 0))

    color_curser1 = (0,255,0)

    pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)

    while True:
        
        screen.fill((0, 0, 0))
        x_curser1 = 320
        y_curser1 = 240

        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # determine if a letter key was pressed
                if event.key == pygame.K_w:
                    mode = 'up'
                elif event.key == pygame.K_s:
                    mode = 'down'
                elif event.key == pygame.K_d:
                    mode = 'right'
                elif event.key == pygame.K_a:
                    mode = 'left'


        color_curser1 = (255,0,0)
        color_curser2 = (255,0,0)
        color_curser3 = (0,0,255)
        color_curser4 = (0,0,255)

        pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)
        
        x_curser1,y_curser1 = curserControl(screen,x_curser1,y_curser1,mode,count,color_curser1,radius)

        pygame.draw.circle(screen, color_curser3, (x_curser1, y_curser1), radius)

        pygame.display.flip()
        
        clock.tick(60)

def curserControl(screen,x_curser1,y_curser1,mode,count,color_curser1,radius):

    publish_velocity=rospy.Publisher('vel', Twist,queue_size=20)
    vel=Twist()


    if mode == 'up':

        vel.linear.x= 1
        publish_velocity.publish(vel)
        vel.linear.x= 0
        y_curser1= y_curser1 -20
        pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)
        print("up")
    elif mode == 'down':
        vel.linear.x= -1
        publish_velocity.publish(vel)
        vel.linear.x= 0
        y_curser1= y_curser1 +20
        pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)
        print("down")
    elif mode == 'right':
        vel.angular.z= -1
        publish_velocity.publish(vel)
        vel.angular.z= 0
        x_curser1= x_curser1 +20
        pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)
        print("right")
    elif mode == 'left':

        vel.angular.z = 1
        publish_velocity.publish(vel)
        vel.angular.z= 0
        x_curser1= x_curser1 -20
        pygame.draw.circle(screen, color_curser1, (x_curser1, y_curser1), radius)  
        print("left")
    
    return x_curser1, y_curser1    
    


main()
