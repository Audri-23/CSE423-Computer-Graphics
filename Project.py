from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import time, random

starting_time=time.time()

# Camera-related variables
camera_pos = (500,0,375)
looking=(0,0,0)
up_vector=(0,0,1)
fovY = 120  # Field of view

GRID_LENGTH = 500
road_segment_start=[600,-600,-1800]
road_segment_end=[-600,-1800,-3000]
ending=-3000
road_half=450
dist=0
play=True
player_pos=(450,0,20)
current_pos="mid"
score=0
h_score=0
score_inc=0
speed=1.5
side=30
cheat=False
fpp=False
top=False
game_over=False
obstacles=[]
start=False
detected=False

for i in range(400,-3000,-200):
    n=random.choice([300,0,-300])
    o=20
    obs_col=(random.random(),random.random(),random.random())
    top_col=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
    obstacles.append((i,n,o,obs_col,top_col))
obstacles[0]=(obstacles[0][0],random.choice([-300,300]),obstacles[0][2],obstacles[0][3],obstacles[0][4])

def draw_cars(args,col,head):
    #car body
    glPushMatrix()
    glColor3f(col[0],col[1],col[2])
    glTranslatef(args[0],args[1],args[2])
    glScalef(1,1,0.5)
    glutSolidCube(60)
    glPopMatrix()
    
    #car tires
    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(args[0]+15,args[1]+22,args[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(args[0]-15,args[1]+22,args[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(args[0]-15,args[1]-22,args[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(args[0]+15,args[1]-22,args[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()


    glPushMatrix()
    glColor3f(col[0],col[1],col[2])
    glTranslatef(args[0],args[1],args[2]+6)
    glScalef(1,1,0.02)
    glutSolidCube(60)
    glPopMatrix()

    #car top
    glPushMatrix()
    glColor3f(head[0],head[0],head[0])
    glTranslatef(args[0],args[1],args[2]+20)
    glScalef(0.6,1,0.2)
    glutSolidCube(60)
    glPopMatrix()

def draw_shapes():
    global player_pos, obstacles
    #car body
    glPushMatrix()
    glColor3f(0,1,1)
    glTranslatef(player_pos[0],player_pos[1],player_pos[2])
    glScalef(1,1,0.5)
    glutSolidCube(60)
    glPopMatrix()
    
    #car tires
    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(player_pos[0]+15,player_pos[1]+22,player_pos[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(player_pos[0]-15,player_pos[1]+22,player_pos[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(player_pos[0]-15,player_pos[1]-22,player_pos[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(player_pos[0]+15,player_pos[1]-22,player_pos[2]-15)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()


    glPushMatrix()
    glColor3f(0,1,1)
    glTranslatef(player_pos[0],player_pos[1],player_pos[2]+6)
    glScalef(1,1,0.02)
    glutSolidCube(60)
    glPopMatrix()

    #car top
    glPushMatrix()
    glColor3f(0.9,0.9,0.9)
    glTranslatef(player_pos[0],player_pos[1],player_pos[2]+20)
    glScalef(0.6,1,0.2)
    glutSolidCube(60)
    glPopMatrix()

    #obstacle cars
    for i in obstacles:
        draw_cars(i,i[3],i[4])



def keyboardListener(key, x, y):
    global player_pos, current_pos, top, play, game_over, score, score_inc, obstacles, road_segment_start, road_segment_end, ending, dist, camera_pos, looking, start, cheat, speed, side
    if start:
        if key == b'a' and play:
            if current_pos!="left":
                if current_pos=="right":
                    current_pos="mid"
                else:
                    current_pos="left"

        if key == b'd' and play:
            if current_pos!="right":
                if current_pos=="left":
                    current_pos="mid"
                else:
                    current_pos="right"

        # Toggle cheat mode (C key)
        if key == b'c':
            cheat=not cheat

        # Top-Down overview (V key)
        if key == b'v':
            top=not top

        # Reset the game if R key is pressed
        if key == b'r' and game_over:
            score=0
            score_inc=0
            road_segment_start=[600,-600,-1800]
            road_segment_end=[-600,-1800,-3000]
            ending=-3000
            dist=0
            speed=1.5
            side=30
            player_pos=(450,0,20)
            current_pos="mid"
            camera_pos=(500,0,375)
            looking=(0,0,0)
            obstacles=[]
            for i in range(400,-3000,-200):
                n=random.choice([300,0,-300])
                o=20
                obs_col=(random.random(),random.random(),random.random())
                top_col=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
                obstacles.append((i,n,o,obs_col,top_col))
            obstacles[0]=(obstacles[0][0],random.choice([-300,300]),obstacles[0][2],obstacles[0][3],obstacles[0][4])
            game_over=False

        if key==b'p' and (not game_over):
            play=not play
    else:
        if key==b' ' and (not start):
            start= True
    
    if key==b'e':
        glutLeaveMainLoop()


def specialKeyListener(key, x, y):
    global camera_pos, start
    if start:
        x, y, z = camera_pos
        # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP and z<=700:
            z+=2

        # # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN and z>=250:
            z-=2
        camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global fpp, start
    if start:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            fpp=not fpp


def setupCamera():
    global camera_pos, looking, fpp, player_pos, up_vector
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    
    if fpp:
        x=player_pos[0]-15
        y=player_pos[1]
        z=player_pos[2]+40
        a=player_pos[0]-50
        b=player_pos[1]
        c=player_pos[2]+30
        d,e,f=up_vector
    else:
        if top:
            x=player_pos[0]
            y=0
            z=350
            a,b,c=player_pos[0],0,0
            d,e,f=(-1,0,0)
        else:
            x, y, z = camera_pos
            a,b,c = looking
            d,e,f=up_vector
    
    gluLookAt(x, y, z,  
              a, b, c,
              d, e, f)


def idle():
    global camera_pos, looking, road_segment_start, road_segment_end, player_pos, score, score_inc, current_pos, ending, obstacles, dist, play, game_over, h_score, start, cheat, detected, speed, side
    if start:
        if play and (not game_over):
            x,y,z=camera_pos
            a,b,c=looking
            if score%100==0 and score!=0 and score<750:
                speed+=0.5
                score_inc+=1
            camera_pos=(x-speed,y,z)
            looking=(a-speed,b,c)
            if current_pos=="left" and player_pos[1]>-300:
                player_pos=(player_pos[0]-speed,player_pos[1]-side,0)
            elif current_pos=="right" and player_pos[1]<300:
                player_pos=(player_pos[0]-speed,player_pos[1]+30,0)
            elif current_pos=="mid" and player_pos[1]!=0:
                if player_pos[1]<0:
                    player_pos=(player_pos[0]-speed,player_pos[1]+side,0)
                else:
                    player_pos=(player_pos[0]-speed,player_pos[1]-side,0)
            else:
                player_pos=(player_pos[0]-speed,player_pos[1],0)

            dist-=speed
            score_inc+=0.03
            score=int(score_inc)

            if dist<=-200:
                obstacles.pop(0)
                n=random.choice([300,0,-300])
                o=20
                obs_col=(random.random(),random.random(),random.random())
                top_col=random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1)
                obstacles.append((ending,n,o,obs_col,top_col))
                ending-=200
                dist=0

            for i in range(4):
                dx=abs(player_pos[0]-obstacles[i][0])
                dy=abs(player_pos[1]-obstacles[i][1])
                if dx<55 and dy<60:
                    game_over=True
                    if score>h_score:
                        h_score=score
            
            if cheat:
                for j in range(4):
                    dx=abs(player_pos[0]-obstacles[j][0])
                    dy=abs(player_pos[1]-obstacles[j][1])
                    if dx<100 and dy<20:
                        if current_pos=="left" or current_pos=="right":
                            current_pos="mid"
                        else:
                            if obstacles[j+1][1]==-300:
                                current_pos="right"
                            else:
                                current_pos="left"
                        break


            if road_segment_end[0] > camera_pos[0]+600:
                for i in range(3):
                    road_segment_start[i]-=1200
                    road_segment_end[i]-=1200

    glutPostRedisplay()


def showScreen():
    global road_segment_start, road_segment_end, road_half, camera_pos, score, cheat, play, game_over, h_score, start
    if start:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, 1000, 800)

        setupCamera()

        #road
        for i in range(3):
            visible_road_start=road_segment_start[i]
            visible_road_end=road_segment_end[i]
            glColor3f(0.2,0.2,0.2)
            glBegin(GL_QUADS)
            glVertex3f(visible_road_start,-road_half,0)
            glVertex3f(visible_road_end,-road_half,0)
            glVertex3f(visible_road_end,road_half,0)
            glVertex3f(visible_road_start,road_half,0)
            glEnd()
            temp=visible_road_start-50
            while temp>visible_road_end:
                glColor3f(0.4,0.26,0.13)
                glBegin(GL_QUADS)
                glVertex3f(temp-10,-road_half,0)
                glVertex3f(temp+10,-road_half,0)
                glVertex3f(temp+10,-road_half,50)
                glVertex3f(temp-10,-road_half,50)

                glVertex3f(temp-10,road_half,0)
                glVertex3f(temp+10,road_half,0)
                glVertex3f(temp+10,road_half,50)
                glVertex3f(temp-10,road_half,50)
                glEnd()

                glColor3f(0,1,0)
                glBegin(GL_TRIANGLES)
                glVertex3f(temp-45,-road_half,50)
                glVertex3f(temp+45,-road_half,50)
                glVertex3f(temp,-road_half,80)

                glVertex3f(temp-45,road_half,50)
                glVertex3f(temp+45,road_half,50)
                glVertex3f(temp,road_half,80)
                glEnd()

                glColor3f(1,1,1)
                glBegin(GL_QUADS)
                glVertex3f(temp+25,310,0)
                glVertex3f(temp-25,310,0)
                glVertex3f(temp-25,290,0)
                glVertex3f(temp+25,290,0)

                glVertex3f(temp+25,10,0)
                glVertex3f(temp-25,10,0)
                glVertex3f(temp-25,-10,0)
                glVertex3f(temp+25,-10,0)

                glVertex3f(temp+25,-310,0)
                glVertex3f(temp-25,-310,0)
                glVertex3f(temp-25,-290,0)
                glVertex3f(temp+25,-290,0)
                glEnd()

                temp-=100

        draw_shapes()

        if game_over:
            draw_text(440, 660, f"Game Over!")
            draw_text(455, 630, f"Score: {score}")
            draw_text(420, 600, f"Highest Score: {h_score}")
            draw_text(422, 550, f"Press r to restart")
            draw_text(430, 520, f"Press e to exit")

        else:
            draw_text(10, 770, f"Score: {score}")
            if cheat:
                draw_text(10, 710, f"Cheat Mode: ON")
            else:
                draw_text(10, 710, f"Cheat Mode: OFF")
            if play:
                draw_text(10, 740, f"Playing")
                draw_text(740,730, f"Press p to pause the game", GLUT_BITMAP_HELVETICA_18)
            else:
                draw_text(10, 740, f"Pasued")
                draw_text(740,730, f"Press p to resume the game", GLUT_BITMAP_HELVETICA_18)
            
            draw_text(740,770, f"Press a/d to move the car", GLUT_BITMAP_HELVETICA_18)
            draw_text(740,750, f"Press v to change the view", GLUT_BITMAP_HELVETICA_18)
            draw_text(740,710, f"Press e to exit", GLUT_BITMAP_HELVETICA_18)
    else:
        draw_text(170, 610, f"READ THE INSTRUCTIONS BEFORE STARTING THE GAME!")
        draw_text(328, 540, f"Press a and d to Move Left and Right")
        draw_text(332, 510, f"Press p to Pause/Resume the Game")
        draw_text(363, 480, f"Press v for Top-Down View")
        draw_text(290, 450, f"Press Up/Down Arrow to Adjust View in TPP")
        draw_text(334, 420, f"Right Click on Mouse for FPP View")
        draw_text(304, 390, f"Press c to Activate/Deactivate Cheat Mode")
        draw_text(398, 320, f"Press SPACE to Start")
        draw_text(435, 280, f"Press e to Exit")
    

    glutSwapBuffers()

def draw_text(x, y, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(480,100)
    wind = glutCreateWindow(b"Infinite Road Traffic Survival Simulator")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()