from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

start_time=time.time()
height, width = 800, 800
catcher_up_x1,catcher_up_x2,catcher_down_x1,catcher_down_x2=322,478,340,460
catcher_up_y,catcher_down_y=28,10
score=0
play=True
diamond_y=737.5
diamond_x=400
r,g,b=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
game_over=False
x,y,z=1,1,1
speed=150
cheat=False
move=True
catcher_speed=8
sp=8

def keyboard_listener(key,x,y):
    global cheat
    if key==b'c':
        cheat=not cheat
        if cheat==True:
            print("Cheat Mode Activated!")
        else:
            print("Cheat Mode Dectivated!")


def special_key_listener(key,x,y):
    global catcher_up_x1,catcher_up_x2,catcher_down_x1,catcher_down_x2,game_over,sp,score
    if score%12==0 and score>0:
        sp+=1
    if play and not game_over:
        if key==GLUT_KEY_RIGHT and catcher_up_x2<=795:
            catcher_up_x1+=sp
            catcher_down_x1+=sp
            catcher_up_x2+=sp
            catcher_down_x2+=sp
        elif key==GLUT_KEY_LEFT and catcher_up_x1>=5:
            catcher_up_x1-=sp
            catcher_down_x1-=sp
            catcher_up_x2-=sp
            catcher_down_x2-=sp
        glutPostRedisplay()

def mouse_listener(button,state,x1,y1):
    global play, game_over, diamond_x,diamond_y,x,y,z,score,r,g,b,speed,catcher_speed,sp
    y1=800-y1
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        if 385<=x1<=422 and 737.5<=y1<=782.5:
            play=not play
        elif 728<=x1<=775 and 737.5<=y1<=785:
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()
        elif 28<=x1<=78 and 737.5<=y1<=785:
            print("Starting over!")
            game_over=False
            score=0
            speed=150
            diamond_y=737.5
            diamond_x=400
            x,y,z=1,1,1
            r,g,b=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
            catcher_speed=8
            sp=8

    glutPostRedisplay()

def setup_projection():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 0, 800, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def display():
    global game_over,r,g,b,catcher_up_x1,catcher_up_x2,catcher_down_x1,catcher_down_x2,catcher_up_x1,catcher_up_x2,catcher_down_x1,catcher_down_x2, diamond_x,diamond_y,x,y,z,catcher_up_y,catcher_down_y

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    setup_projection()

    #replay buttor
    create_line(30,760,75,760,0,1,1)
    create_line(30,760,52.5,782.5,0,1,1)
    create_line(30,760,52.5,737.5,0,1,1)

    #exit button
    create_line(730,782.5,775,737.5,1,0,0)
    create_line(730,737.5,775,782.5,1,0,0)

    #play-pause button
    if play:
        create_line(390,782.5,390,737.5,1,0.75,0)
        create_line(410,782.5,410,737.5,1,0.75,0)
    else:
        create_line(385,778.75,385,741.25,1,0.75,0)
        create_line(385,778.75,422,760,1,0.75,0)
        create_line(385,741.25,422,760,1,0.75,0)


    #catcher
    create_line(catcher_down_x1,catcher_down_y,catcher_down_x2,catcher_down_y,x,y,z)
    create_line(catcher_up_x1,catcher_up_y,catcher_up_x2,catcher_up_y,x,y,z)
    create_line(catcher_up_x1,catcher_up_y,catcher_down_x1,catcher_down_y,x,y,z)
    create_line(catcher_down_x2,catcher_down_y,catcher_up_x2,catcher_up_y,x,y,z)

    #diamonds
    if not game_over:
        create_line(diamond_x,diamond_y,diamond_x+20,diamond_y-20,r,g,b)
        create_line(diamond_x,diamond_y-40,diamond_x+20,diamond_y-20,r,g,b)
        create_line(diamond_x,diamond_y,diamond_x-20,diamond_y-20,r,g,b)
        create_line(diamond_x-20,diamond_y-20,diamond_x,diamond_y-40,r,g,b)

    glutSwapBuffers()



def create_line(x1,y1,x2,y2,*colours):
    zone=FindZone(x1,y1,x2,y2)
    x1,y1=convertToZero(x1,y1,zone)
    x2,y2=convertToZero(x2,y2,zone)
    dx=x2-x1
    dy=y2-y1
    d=(dy*2)-dx
    incrE=dy*2
    incrNE=(dy-dx)*2
    glColor3f(colours[0], colours[1], colours[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    while x1<=x2:
        draw_x,draw_y=convertFromZero(x1,y1,zone)
        glVertex2f(draw_x,draw_y)
        x1+=1
        if d>0:
            y1+=1
            d+=incrNE
        else:
            d+=incrE
    glEnd()
    
    

def FindZone(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if abs(dx)>abs(dy):
        if dx>0 and dy>=0:
            return 0
        elif dx<0 and dy>=0:
            return 3
        elif dx<0 and dy<0:
            return 4
        elif dx>0 and dy<0:
            return 7
    else:
        if dx>=0 and dy>0:
            return 1
        elif dx<0 and dy>0:
            return 2
        elif dx<0 and dy<0:
            return 5
        elif dx>=0 and dy<0:
            return 6



def convertToZero(x,y,zone):
    if zone==0:
        return (x,y)
    elif zone==1:
        return (y,x)
    elif zone==2:
        return (y,-x)
    elif zone==3:
        return (-x,y)
    elif zone==4:
        return (-x,-y)
    elif zone==5:
        return (-y,-x)
    elif zone==6:
        return (-y,x)
    elif zone==7:
        return (x,-y)
    


def convertFromZero(x,y,zone):
    if zone==0:
        return (x,y)
    elif zone==1:
        return (y,x)
    elif zone==2:
        return (-y,x)
    elif zone==3:
        return (-x,y)
    elif zone==4:
        return (-x,-y)
    elif zone==5:
        return (-y,-x)
    elif zone==6:
        return (y,-x)
    elif zone==7:
        return (x,-y)
    

def animate():
    global start_time,speed,play,diamond_x,diamond_y,score,game_over,r,g,b,x,y,z,catcher_up_x1,catcher_up_x2,catcher_down_x1,catcher_down_x2,catcher_up_y,catcher_down_y,cheat,move,catcher_speed
    
    present_time=time.time()
    change=present_time-start_time
    start_time=present_time
    if play and not game_over:
        diamond_y-=(speed*change)
        diamond_top=diamond_y
        diamond_bottom=diamond_y-40
        diamond_left=diamond_x-20
        diamond_right=diamond_x+20
        if (diamond_bottom)<=catcher_up_y:
            if diamond_left<catcher_up_x2 and diamond_right>catcher_up_x1 and diamond_bottom<catcher_up_y and diamond_top>catcher_down_y:
                score+=1
                if score%4==0 and score!=0:
                    speed+=50
                print(f"Score: {score}")
                r,g,b=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
                diamond_y=737.5
                diamond_x=random.uniform(22,778)
            elif diamond_bottom+20<=catcher_down_y:
                game_over=not game_over
                x,y,z=1,0,0
                print(f"Game Over! Score: {score}")

    if cheat:
        if catcher_up_x1<diamond_x and catcher_up_x2-35<diamond_x:
            if score%190==0 and score!=0:
                catcher_speed+=3         
            if catcher_up_x2<=795:
                catcher_up_x1+=catcher_speed
                catcher_up_x2+=catcher_speed
                catcher_down_x1+=catcher_speed
                catcher_down_x2+=catcher_speed
        elif catcher_up_x1+35>diamond_x and catcher_up_x2>diamond_x:
            if catcher_up_x1>=5:
                catcher_up_x1-=catcher_speed
                catcher_up_x2-=catcher_speed
                catcher_down_x1-=catcher_speed
                catcher_down_x2-=catcher_speed

    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA)
    glutInitWindowSize(height, width)
    glutInitWindowPosition(600, 100)
    glutCreateWindow(b"Catch The Diamonds!")
    glutDisplayFunc(display)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutIdleFunc(animate)

    glutMainLoop()

if __name__=="__main__":
    main()