from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


width, height=800,800

rain_shift=0

rain_drop_x=[123, -45, 378, -222, 0, 199, -400, 77, 305, -168, 400, -99, 210, 56, -301, 189, -255, 88, -77, 399, -300, -300, 250, -350, -225, -330, -375, 200, 370, 50, 110, -120, -260, 210, 300, -310, -220, -130, -40, 50, 140, 230, 320, 380, -380, -95, -250, -130, -370, -200, -280, -15, -330, -50, -360, -10, -290, -75, -145, -310, -225, -390, -5, -160, -340, 100, 150, 250, 30, 175, 315, -250, -170, -134, -320, -90, -250, 293, 360, 234, 196, -132, -253, 293, 143, 188, -314, -100, -172, -235, -359]

rain_drop_x1=[123, -45, 378, -222, 0, 199, -400, 77, 305, -168, 400, -99, 210, 56, -301, 189, -255, 88, -77, 399, -300, -300, 250, -350, -225, -330, -375, 200, 370, 50, 110, -120, -260, 210, 300, -310, -220, -130, -40, 50, 140, 230, 320, 380, -380, -95, -250, -130, -370, -200, -280, -15, -330, -50, -360, -10, -290, -75, -145, -310, -225, -390, -5, -160, -340, 100, 150, 250, 30, 175, 315, -250, -170, -134, -320, -90, -250, 293, 360, 234, 196, -132, -253, 293, 143, 188, -314, -100, -172, -235, -359]

rain_drop_y=[247, -382, 119, 301, -44, 75, -268, 0, 192, -399, 88, 354, -176, 220, -315, 64, 400, -243, 189, -57, -300, 300, 100, 200, 150, 110, 350, 300, 330, 320, 105, 75, 5, -37, -67, 310, 220, 130, 40, -50, -140, -230, -320, -380, 380, -5, -290, -75, -145, -310, -225, -390, -8, -160, -340, -90, -250, -130, -370, -200, -280, -15, -330, -50, -360, -325, -375, -350, -300, -270, -175, -100, -120, -193, -65, -274, -343, -250, -98, -101, 197, 263, 360, 356, 373, 188, -74, -303, -288, -156, -241]

rain_drop_y1=[]
for i in rain_drop_y:
    rain_drop_y1.append(i-22)


def setup_projection():
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400,400,-400,400,0,1)
    glMatrixMode(GL_MODELVIEW)


ani=False
c=0
current="n"

def keyboard_listener(key,x,y):

    global ani,current

    if (key==b"n" or key==b"N") and current=="d":
        ani=True     
    elif (key==b"d" or key==b"D") and current=="n":
        ani=True


def special_key_listener(key, x,y):
    global rain_shift, rain_drop_x1
    if key==GLUT_KEY_RIGHT:
        if rain_shift<20:
            rain_shift+=5
            for i in range(len(rain_drop_x1)):
                rain_drop_x1[i]+=5
    elif key==GLUT_KEY_LEFT:
        if rain_shift>-20:
            rain_shift-=5
            for i in range(len(rain_drop_x1)):
                rain_drop_x1[i]-=5
    
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    setup_projection()

    glColor3f(1,1,0)
    glPointSize(100)
    glBegin(GL_POINTS)
    glVertex2f(0,0)
    glEnd()

    # Background
    glColor3f(0.6196,0.4353,0.1216)
    glBegin(GL_TRIANGLES)
    glVertex2f(-400,100)
    glVertex2f(400,100)
    glVertex2f(-400,-400)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(400,100)
    glVertex2f(400,-400)
    glVertex2f(-400,-400)
    glEnd()

    # tree
    tree_x0=-400
    tree_x1=-320
    for i in range(10):
        glColor3f(0.2,1,0.2)
        glBegin(GL_TRIANGLES)
        glVertex2f(tree_x0,0)
        glVertex2f(tree_x1,0)
        glColor3f(0.6196,0.4353,0.1216)
        glVertex2f((tree_x0+40),100)
        glEnd()
        tree_x0=tree_x1
        tree_x1+=80
    
    # house
         # walls
    glColor3f(1,1,0.8)
    glBegin(GL_TRIANGLES)
    glVertex2f(-180,50)
    glVertex2f(180,50)
    glVertex2f(-180,-150)
    glEnd()

    glColor3f(1,1,0.8)
    glBegin(GL_TRIANGLES)
    glVertex2f(180,50)
    glVertex2f(180,-150)
    glVertex2f(-180,-150)
    glEnd()

         # roof
    glColor3f(0.4,0,0.8)
    glBegin(GL_TRIANGLES)
    glVertex2f(-210,50)
    glVertex2f(210,50)
    glVertex2f(0,150)
    glEnd()

         # door
    glColor3f(0.2,0.6,1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-25,-150)
    glVertex2f(-25,-50)
    glVertex2f(25,-50)
    glEnd()
    
    glColor3f(0.2,0.6,1)
    glBegin(GL_TRIANGLES)
    glVertex2f(25,-50)
    glVertex2f(25,-150)
    glVertex2f(-25,-150)
    glEnd()

    glColor3f(0,0,0)
    glPointSize(7)
    glBegin(GL_POINTS)
    glVertex2f(15,-100)
    glEnd()

        # windows
    glColor3f(0.2,0.6,1)
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(-95,-35)
    glEnd()
    glColor3f(0,0,0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(-95,-10)
    glVertex2f(-95,-60)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(-120,-35)
    glVertex2f(-70,-35)
    glEnd()

    glColor3f(0.2,0.6,1)
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(92.5,-35)
    glEnd()
    glColor3f(0,0,0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(92.5,-11)
    glVertex2f(92.5,-61)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(68,-35)
    glVertex2f(118.5,-35)
    glEnd()


         # rain drops
    for i in range(len(rain_drop_x)):
        rain_drop(rain_drop_x[i],rain_drop_x1[i],rain_drop_y[i],rain_drop_y1[i])

    glutSwapBuffers()



def rain_drop(rain_x,rain_x1,rain_y0,rain_y1):
    glColor3f(0.6, 0.74, 0.86)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(rain_x,rain_y0)
    glVertex2f(rain_x1,rain_y1)
    glEnd()


def animate():
    global rain_drop_x1, rain_drop_y, rain_drop_x, rain_shift, rain_drop_y1, ani, c, current

    if ani==True and c<=1 and current=="d":
        c-=0.001
        glClearColor(c,c,c,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if c<0:
            ani=False
            current="n"
            c=0
    elif ani==True and c>=0 and current=="n":
        c+=0.001
        glClearColor(c,c,c,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if c>1:
            ani=False
            current="d"
            c=1    

    for i in range(len(rain_drop_x)):
        if rain_shift==0:
            rain_drop_y[i]=(rain_drop_y[i]-0.25)
            rain_drop_y1[i]=(rain_drop_y1[i]-0.25)
            if rain_drop_y[i]<-400:
                rain_drop_y[i]=400
                rain_drop_y1[i]=400-22
        elif rain_shift!=0:
            slope=(rain_drop_y1[i]-rain_drop_y[i])/(rain_drop_x1[i]-rain_drop_x[i])
            slope=round(slope,1)
            inter=rain_drop_y[i]-(slope*rain_drop_x[i])
            rain_drop_y[i]-=0.25
            rain_drop_x[i]=(rain_drop_y[i]-inter)/slope
            rain_drop_y1[i]-=0.25
            rain_drop_x1[i]=(rain_drop_y1[i]-inter)/slope
            if rain_drop_y[i]<-400 or rain_drop_x[i]>400 or rain_drop_x[i]<=-400:
                if slope<0:
                    x1, y1, y2=-400, 400, -400
                    x2=((y2-y1)/slope)+x1
                    if rain_drop_x[i]>=x2:
                        rain_drop_y[i]=400
                        rain_drop_x[i]=(rain_drop_y[i]-inter)/slope
                        rain_drop_y1[i]=400-22
                        rain_drop_x1[i]=(rain_drop_y1[i]-inter)/slope
                    elif rain_drop_x[i]<x2:
                        rain_drop_x[i]=-400
                        rain_drop_y[i]=(slope*rain_drop_x[i])+inter
                        rain_drop_y1[i]=rain_drop_y[i]-22
                        rain_drop_x1[i]=(rain_drop_y1[i]-inter)/slope
                elif slope>0:
                    x1, y1, y2=400, 400, -400
                    x2=((y2-y1)/slope)+x1
                    if rain_drop_x[i]>=x2:
                        rain_drop_x[i]=400
                        rain_drop_y[i]=(slope*rain_drop_x[i])+inter
                        rain_drop_y1[i]=rain_drop_y[i]-22
                        rain_drop_x1[i]=(rain_drop_y1[i]-inter)/slope
                    elif rain_drop_x[i]<x2:
                        rain_drop_y[i]=400
                        rain_drop_x[i]=(rain_drop_y[i]-inter)/slope
                        rain_drop_y1[i]=400-22
                        rain_drop_x1[i]=(rain_drop_y1[i]-inter)/slope

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(height,width)
    glutInitWindowPosition(600,100)
    glutCreateWindow(b"House in Rainfall")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutIdleFunc(animate)
    glutMainLoop()


if __name__=="__main__":
    main()