from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24
import math, random

camera_pos = (500,0,500)
camera_init=(500,0,500)
fovY = 120
GRID_LENGTH = 600
cam_ang=0
player_ang=0
rem_life=5
score, missed_bullets= 0,0
enemy_pos=[]
for i in range(5):
    tup=(random.uniform(-580,580),random.uniform(-580,580))
    enemy_pos.append(tup)
enemy_scale=1
sign=1
trans=(0, 0, 0)
looking=(0,0,0)
fpp=False
bullets=[]
missed_bullet_pos=[]
game_over=False
enemy_killed=[]
cheat=False
cheat_vision=False
temp_list=[]

print(f"Remaining Player Life: {rem_life}")

def draw_text(x, y, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():
    global trans, player_ang, enemy_pos, enemy_scale, game_over
    #enemy
    if not game_over:
        for i in enemy_pos:
            glPushMatrix()
            glColor3f(1,0,0)
            glTranslatef(i[0], i[1], 0)
            glScalef(enemy_scale, enemy_scale, enemy_scale)
            gluSphere(gluNewQuadric(), 35, 10, 10)
            glColor3f(0,0,0)
            glTranslatef(0,0,30)
            gluSphere(gluNewQuadric(), 15, 10, 10)
            glPopMatrix()

    glPushMatrix()

    #body
    glColor3f(0.3, 0.46, 0.32)
    glTranslatef(trans[0],trans[1],trans[2])
    if game_over:
          fall_x=-math.sin(math.radians(player_ang))
          fall_y=math.cos(math.radians(player_ang))
          glRotatef(90,fall_x,fall_y,0)
    glTranslatef(0, 0, 25)
    glScalef(1.8,1.8,2)
    glRotatef(player_ang,0,0,1)
    glutSolidCube(22)

    #legs
    glColor3f(0,0,1)
    glTranslatef(0,-8.5,-11)
    glScalef(1,1/1.5,2.2)
    glRotatef(180,0,10,0)
    gluCylinder(gluNewQuadric(), 9, 2, 5, 10, 10)
    glTranslatef(0,25.5,0)
    gluCylinder(gluNewQuadric(), 9, 2, 5, 10, 10)

    glPopMatrix()
    glPushMatrix()

    #gun
    glColor3f(0.7,0.75,0.71)
    glTranslatef(trans[0],trans[1],trans[2])
    glRotatef(player_ang,0,0,1)
    if game_over:
          fall_x=-math.sin(math.radians(player_ang))
          fall_y=math.cos(math.radians(player_ang))
          glRotatef(90,0,1,0)
    glTranslatef(-60,0,36)
    glRotatef(90,0,1,0)
    gluCylinder(gluNewQuadric(), 3, 8, 40, 10, 10)
    
    glPopMatrix()
    glPushMatrix()

    #left hand
    glColor3f(0.91,0.78,0.65)
    glTranslatef(trans[0],trans[1],trans[2])
    glRotatef(player_ang,0,0,1)
    if game_over:
          fall_x=-math.sin(math.radians(player_ang))
          fall_y=math.cos(math.radians(player_ang))
          glRotatef(90,0,1,0)
    glTranslatef(-50,-22,38)
    glRotatef(90,0,1,0)
    gluCylinder(gluNewQuadric(), 2, 8, 30, 10, 10)

    glPopMatrix()
    glPushMatrix()

    #right hand
    glTranslatef(trans[0],trans[1],trans[2])
    glRotatef(player_ang,0,0,1)
    if game_over:
          fall_x=-math.sin(math.radians(player_ang))
          fall_y=math.cos(math.radians(player_ang))
          glRotatef(90,0,1,0)
    glTranslatef(-50,22,38)
    glRotatef(90,0,1,0)
    gluCylinder(gluNewQuadric(), 2, 8, 30, 10, 10)

    glPopMatrix()
    glPushMatrix()

    #head
    glColor3f(0,0,0)
    glTranslatef(trans[0],trans[1],trans[2])
    glRotatef(player_ang,0,0,1)
    if game_over:
          fall_x=-math.sin(math.radians(player_ang))
          fall_y=math.cos(math.radians(player_ang))
          glRotatef(90,0,1,0)
    glTranslatef(0,0,60)    
    gluSphere(gluNewQuadric(), 16, 10, 10)

    glPopMatrix()   


def keyboardListener(key, x, y):
    global trans, player_ang, game_over, score, missed_bullets, rem_life, cheat, cheat_vision
    if not game_over:
        if key == b'w':
            a,b,c=trans
            a-=(10*math.cos(math.radians(player_ang)))            
            b-=(10*math.sin(math.radians(player_ang)))
            if not (-GRID_LENGTH<a<GRID_LENGTH and -GRID_LENGTH<b<GRID_LENGTH):
                a=trans[0]
                b=trans[1]
            trans=(a,b,c)

        if key == b's':
            a,b,c=trans
            a+=(10*math.cos(math.radians(player_ang)))            
            b+=(10*math.sin(math.radians(player_ang)))
            if not (-(GRID_LENGTH-50)<a<(GRID_LENGTH+60) and -(GRID_LENGTH-50)<b<(GRID_LENGTH-50)):
                a=trans[0]
                b=trans[1]
            trans=(a,b,c)


        if key == b'a':
            player_ang+=5

        if key == b'd':
            player_ang-=5

        if key == b'c':
            cheat=not cheat

        if key == b'v':
            cheat_vision=not cheat_vision

    if key == b'r' and game_over:
        score=0
        missed_bullets=0
        rem_life=5
        print(f"Remaining Player Life: {rem_life}")
        game_over=False

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_pos, cam_ang
    if (not fpp):
        x, y, z = camera_pos
        if key == GLUT_KEY_UP:
            if z<600:
                z+=3

        if key == GLUT_KEY_DOWN:
            if z>4:
                z-=3

        if key == GLUT_KEY_LEFT:
            cam_ang-=0.01
            x=(500*(math.cos(cam_ang)))
            y=(500*(math.sin(cam_ang)))

        if key == GLUT_KEY_RIGHT:
            cam_ang+=0.01
            x=(500*(math.cos(cam_ang)))
            y=(500*(math.sin(cam_ang)))
        camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global trans, camera_pos, fpp, bullets, player_ang, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        m,n,o=trans
        bullets.append((m,n,player_ang))
        print("Player Bullet Fired!")

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over:
        fpp=not fpp

def setupCamera():
    global camera_pos, looking, fpp, trans, player_ang, cheat_vision, camera_init
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fpp:
        if not cheat_vision:
            x=trans[0]-(20*math.cos(math.radians(player_ang)))
            y=trans[1]-(20*math.sin(math.radians(player_ang)))
            z=trans[2]+55
            a=(trans[0])-(1000*math.cos(math.radians(player_ang)))
            b=trans[1]-(1000*math.sin(math.radians(player_ang)))
            c=trans[2]+50
            camera_init=(x,y,z)
            looking=(a,b,c)
        else:
            a,b,c=looking
            x,y,z=camera_init
        
        gluLookAt(x, y, z,
                a, b, c,
                0, 0, 1)
        
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z,
                0, 0, 0,
                0, 0, 1)
        

def idle():
    global enemy_scale, sign, bullets, GRID_LENGTH, missed_bullets, missed_bullet_pos, game_over, enemy_killed, score, trans, rem_life, enemy_pos, cheat, player_ang, temp_list

    if not game_over:
        if enemy_scale>1.5:
            sign=-1
        if enemy_scale<1:
            sign=1
        enemy_scale+=(0.003*sign)
        temp1=enemy_scale*45
        for i in range(len(bullets)):
            m,n,o=bullets[i]
            m-=(5*math.cos(math.radians(o)))
            n-=(5*math.sin(math.radians(o)))
            if (not (-GRID_LENGTH<=m<=GRID_LENGTH)) or (not (-GRID_LENGTH<=n<=GRID_LENGTH)):
                missed_bullets+=1
                missed_bullet_pos.append((m,n,o))
                print(f"Bullet Missed: {missed_bullets}")
            else:
                for j in enemy_pos:
                    px=m-j[0]
                    py=n-j[1]
                    dis=math.sqrt((px*px)+(py*py))
                    if dis<=temp1:
                        score+=1
                        enemy_killed.append(j)
                        missed_bullet_pos.append((m,n,o))
                        break
            bullets[i]=(m,n,o)
        if missed_bullets==10:
            game_over= True
        for i in enemy_killed:
            if i in enemy_pos:
                enemy_pos.remove(i)
        enemy_killed=[]

        for k in range(len(enemy_pos)):
            p_area=25
            e_area=enemy_scale*25
            px=trans[0]-enemy_pos[k][0]
            py=trans[1]-enemy_pos[k][1]
            dis=math.sqrt((px*px)+(py*py))
            if dis<=(p_area+e_area) or dis==0:
                enemy_killed.append(enemy_pos[k])
                if cheat:
                    score+=1
                    print("Player Bullet Fired!")
                else:
                    rem_life-=1
                    print(f"Remaining Player Life: {rem_life}")
            else:
                bool=False
                epx,epy=enemy_pos[k]
                if enemy_pos[k] in temp_list:
                    temp_list.remove(enemy_pos[k])
                    bool=True
                angle=math.atan2(py,px)
                epx+=(0.1*math.cos(angle))
                epy+=(0.1*math.sin(angle))
                enemy_pos[k]=(epx,epy)
                if bool:
                    temp_list.append((epx,epy))
        if rem_life==0:
            game_over=True

        for i in missed_bullet_pos:
            bullets.remove(i)
        
        missed_bullet_pos=[]
        
        if len(enemy_pos)<5:
            tup=(random.uniform(-580,580),random.uniform(-580,580))
            enemy_pos.append(tup)
        
        if cheat:
            player_ang+=1
            for i in enemy_pos:
                temp_pang=player_ang%360
                up=temp_pang+3
                down=temp_pang-3
                if down<0:
                    down=360+down
                epx,epy=i
                px=epx-trans[0]
                py=epy-trans[1]
                e_ang=(math.degrees(math.atan2(py,px)))+180
                if down<=e_ang<=up:
                    if i not in temp_list:
                        m,n,o=trans
                        bullets.append((m,n,player_ang))
                        temp_list.append(i)
                        print("Player Bullet Fired!")
                        break
            an_temp_list=[]
            for i in temp_list:
                if i not in enemy_pos:
                    an_temp_list.append(i)
            for i in an_temp_list:
                temp_list.remove(i)
                
    else:
        bullets=[]
        missed_bullet_pos=[]
        enemy_killed=[]
        enemy_pos=[]

    glutPostRedisplay()


def showScreen():
    global rem_life, score, missed_bullets, bullets, game_over, score

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    glBegin(GL_QUADS)
    grid_x,grid_y=GRID_LENGTH,GRID_LENGTH
    temp=(GRID_LENGTH*2)/13
    for i in range(13):
        for j in range(13):
            if (i%2==0 and j%2==0) or (i%2!=0 and j%2!=0):
                glColor3f(1,1,1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            glVertex3f((grid_x),grid_y,0)
            glVertex3f((grid_x),(grid_y-temp),0)
            glVertex3f((grid_x-temp),(grid_y-temp),0)
            glVertex3f((grid_x-temp),grid_y,0)
        
            grid_x-=temp
        grid_x=GRID_LENGTH
        grid_y=grid_y-temp
    #borders
    glColor3f(0,1,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,50)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,50)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)

    glColor3f(1,1,1)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,50)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,50)

    glColor3f(0,1,1)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,50)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,50)

    glColor3f(0,0,1)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,50)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,50)

    glEnd()

    glPointSize(4)
    glColor3f(1,0,0)
    for i in bullets:
        glBegin(GL_POINTS)
        glVertex3f(i[0],i[1],40)
        glEnd()

    if not game_over:
        draw_text(10, 750, f"Player Life Remaining: {rem_life}")
        draw_text(10, 720, f"Game Score: {score}")
        draw_text(10, 690, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, 750, f"Game is over. Your score is {score}") 
        draw_text(10, 720, f"Press \"R\" to RESTART the game.")

    draw_shapes()

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(500, 100)
    wind = glutCreateWindow(b"Bullet Frenzy")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()