from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

height, width = 800,800
lst=[0.01,-0.01]
point_x=[]
point_y=[]
col=[]
dir_x=[]
dir_y=[]
speed=0
black=False
freeze=False
rand=0
temp=False

def mouse_listener(button, state, x,y):
    global point_x, point_y, black, dir_x, dir_y, lst, col, freeze

    if not freeze:
        if button== GLUT_RIGHT_BUTTON and state==GLUT_DOWN:
            point_x.append(x)
            point_y.append(800-y)
            dir_x.append(random.choice(lst))
            dir_y.append(random.choice(lst))
            col.append((random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)))

        elif button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
            black=not black

def keyboard_listener(key, x,y):
    global freeze
    if key==b" ":
        freeze=not freeze

def special_key_listener(key,x,y):
    global speed, freeze
    if not freeze:
        if key==GLUT_KEY_UP and speed<15:
            speed+=4
        elif key==GLUT_KEY_DOWN and speed!=0:
            speed-=4

def setup_projection():
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,800,0,800,0,1)
    glMatrixMode(GL_MODELVIEW)

def display():
    global col, rand, temp
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    setup_projection()

    # point creation
    
    if black:
        if rand%3000==0:
            temp= not temp
        rand+=1


    for i in range(len(point_x)):
        if black and (not freeze):
            if temp:
                glColor3f(0,0,0)
            else:
                glColor3f(col[i][0], col[i][1], col[i][2])
        else:
            rand=0
            glColor3f(col[i][0], col[i][1], col[i][2])
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex2f(point_x[i],point_y[i])
        glEnd()
    

    glutSwapBuffers()

def animate():
    global point_x, point_y, dir_x, dir_y, speed, freeze
    if not freeze:
        for i in range(len(point_x)):
            point_x[i]=point_x[i]+dir_x[i]+(speed*dir_x[i])
            point_y[i]=point_y[i]+dir_y[i]+(speed*dir_y[i])
            if point_y[i]>=800 or point_y[i]<=0:
                dir_y[i]*=(-1)
            elif point_x[i]>=800 or point_x[i]<=0:
                dir_x[i]*=(-1)

    glutPostRedisplay()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(height,width)
    glutInitWindowPosition(600,100)
    glutCreateWindow(b"Amazing Box")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()


if __name__=="__main__":
    main()