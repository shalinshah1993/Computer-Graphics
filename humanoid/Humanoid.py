"""
#####################################
## IT 441 Computer Graphics
## Instructor:Nitin Raje
## Implemented By: Shalin Shah
## ID : 201101179
#####################################
"""

import string
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from PIL import Image
import pygame
import pygame.mixer

z_rotate= x_rotate = 0.0
y_rotate = 300.0
fly = 0.0
increase = 0.1
eye = 1.0
modeB = -1.0
angle = 5.0

texture_num = 2.0

x_land = z_land = 0.0
theta = 0.0

def InitGL(Width, Height):
    """
    This is the first method called after instantiating the glutInit Frame. Here, we need to load smooth textures for quadratics object then we 
    set perpective, clear color and lights. We take width and height here because we want to set the aspect ratio in gluPerspective.
    """
    global quadratic, sounds_thrust
    
    # Load all the Textures first
    LoadTextures(9)

    quadratic = gluNewQuadric()
    gluQuadricNormals(quadratic, GLU_SMOOTH)        
    gluQuadricTexture(quadratic, GL_TRUE)           
 
    glEnable(GL_TEXTURE_2D)
    glClearColor(0, 0, 0, 0)    
    glClearDepth(1.0)           
    glDepthFunc(GL_LESS)            
    glEnable(GL_DEPTH_TEST)         
    glShadeModel(GL_SMOOTH)         
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                                    
    gluPerspective(60.0, float(Width)/float(Height), 0.1, 100.0)

    #Set the lightning.
    glMatrixMode(GL_MODELVIEW)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.15, 0.15, 0.15, 0.1))       
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))      
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 0.0, 0.0)) 
    glEnable (GL_LIGHT0)
    glLight (GL_LIGHT0,GL_POSITION,(200,200,0,0))
    glEnable (GL_LIGHTING)

    #initialize all imported pygame modules
    pygame.init()
    #Create a new Sound object from a file
    sounds = pygame.mixer.Sound("imperial.wav")
    sounds_thrust = pygame.mixer.Sound("thrust.wav") 
    sounds.play()

def CreateTexture(imagename, number):
    """
    To create a texture open image, transfer image to string buffer, bind it with an ID and set the texture using glTextImage2D.
    """
    global textures

    image = Image.open(imagename)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)

    glBindTexture(GL_TEXTURE_2D, int(textures[number]))   

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    #The texture magnification function is used when the pixel being textured maps to an area less than or equal to one texture element.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #The texture minifying function is used whenever the pixel being textured maps to an area greater than one texture element.
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    

def CreateLinearFilteredTexture(imagename, number):
    """
    This method is same as above. ONly difference is the TexParameter for magnification and minifying parameters are set to linear filtering.
    """
    global textures

    image = Image.open(imagename)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)

    glBindTexture(GL_TEXTURE_2D, int(textures[number]))   
    #Weighted average of the four texture elements that are closest to the center of the pixel is obtained by LINEAR. Reason for this is better look.
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)


def LoadTextures(number):
    """
    Here we generate 9 ID's for mapping them with textures and then create textures.
    """
    global texture_num, textures

    textures = glGenTextures(number)
    CreateLinearFilteredTexture("head.jpg", 1)
    CreateLinearFilteredTexture("a.jpg", 2)
    CreateLinearFilteredTexture("grnd.jpg", 3)
    CreateTexture("saber.jpg", 8)
    CreateTexture("sky.jpg", 4)
    
    CreateTexture("body.jpg",5)
    CreateLinearFilteredTexture("eyee.jpg",6)


def display():
    """
    This is the main display function where in the entire humnoid is drawn or redrawn. Double buffer is used so we have to swap buffers after 
    re-drawing the new humanoid. Everything here is a cube, the sky ground and humanoid's almost all body parts. A texture is added to that cube.
    """
    global x_rotate, y_rotate, z_rotate, textures, texture_num, fly, increase
    global  x_land, z_land, theta
    glEnable(GL_LIGHTING)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()                    
    gluLookAt(0.0, 4.0, 14.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotatef(x_rotate, 1, 0, 0)
    glRotatef(y_rotate, 0, 1, 0)

    glBindTexture(GL_TEXTURE_2D, int(textures[4]))
        
    glPushMatrix();
    glTranslatef (0, 70.0, 0);

    DrawCube(140.0, 1.0, 140.0);
    glPopMatrix();
    
    glPushMatrix();
    glTranslatef (-70, 70.0, 0);
    #glRotatef(90,0,1,0)
    DrawCube(1.0, 140.0, 140.0);
    glPopMatrix();
    
    glPushMatrix();
    glTranslatef (70, 70.0, 0);
    #glRotatef(90,0,1,0)
    DrawCube(1.0, 140.0, 140.0);
    glPopMatrix();

    glPushMatrix();
    glTranslatef (0.0, 70.0, -70);
    #glRotatef(90,0,1,0)
    DrawCube(140.0, 140.0, 1.0);
    glPopMatrix();
    
    glPushMatrix();
    glTranslatef (0.0, 70.0, 70);
    #glRotatef(90,0,1,0)
    DrawCube(140.0, 140.0, 1.0);
    glPopMatrix();

    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, int(textures[3]))
    glRotatef(theta, 0, 1, 0)
    glTranslatef(x_land, -7.8, z_land)
    DrawCube(140, 1, 140)

    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -.7, 0)
    glTranslatef(0, fly, 0)
    if (fly >= 5 and fly <= 5.1): increase =.005
    if (fly >= 5.5): increase =-.005
    if (fly >= .1):fly = fly + increase
    
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(1, .2, 1)
    glPopMatrix()
    

    glPushMatrix()
    glTranslatef(0, -1.4, 0)
    glTranslatef(0, fly, 0)
    if (fly >= 5 and fly <= 5.1): increase=.005
    if (fly >= 5.5): increase =- .005
    if (fly >= .1): fly = fly + increase
    
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(1, .2, 1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -2.3, 0)
    glTranslatef(0, fly, 0)
    if (fly >= 5 and fly <=5.1 ):increase=.005
    if (fly >= 5.5): increase =- .005
    if (fly >= .1): fly = fly + increase
    
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(.5 , .2, .5)
    glPopMatrix()
    
    glTranslatef(0, fly, 0)
    if (fly >= 5 and fly <= 5.1): increase = .005
    if (fly >= 5.5): increase =- .005
    if (fly >= .1): fly = fly + increase

    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(.7, 1.1, .7)
    
 #head
    glPushMatrix()         
    glTranslatef(0, 0.8, 0)
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))

    gluSphere(quadratic, 0.7, 64, 64)
    glBindTexture(GL_TEXTURE_2D, int(textures[6]))
    glTranslatef(-.2, 0.3, -0.5)
    glRotatef(eye, 1, 0, 0);
    gluSphere(quadratic, .2, 64, 64)

    glTranslatef(0.4,0.0,0)
    gluSphere(quadratic, 0.2, 64, 64)
    glPopMatrix()
  
#right arm     
    glPushMatrix()          
    glTranslatef(1.5,0,0)
    if(modeB == -1):
        glRotatef(z_rotate, 1, 0, 0)
    
    glRotatef(-4 * fly, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(0.25, 1, 0.3)
    glTranslatef(0, -2.2, 0)
    glRotatef(10 * fly, 1, 0, 0)
    
    if(modeB == -1):
        if(z_rotate < 180):
            glRotatef(z_rotate, 1, 0, 0)
        else:
            glRotatef(360-z_rotate,1,0,0)
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(0.2, 1, 0.2)

    
    if(fly >= .1):
        glTranslatef(0, -1.5, 0)
        #glRotatef(360-20*fly,1,0,0)
        if(fly >= 4):
            glScalef(1.5 + increase * 20, 1.5 + increase * 20, 1.5 + increase * 20)
        glBindTexture(GL_TEXTURE_2D, int(textures[8]))
        DrawCube(0.1, 2.5, 0.1)
    glPopMatrix()
    

#left arm 
    glPushMatrix()          
    glTranslatef(-1.5, 0, 0)
    glRotatef(-4 * fly, 1, 0, 0)
    if (modeB == -1):
        glRotatef(360 - z_rotate, 1, 0, 0)
    
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(0.25, 1, 0.3)
    glTranslatef(0, -2.2, 0)
    glRotatef(10 * fly, 1, 0, 0)
    
    if modeB == -1:
        if (z_rotate < 180):
            glRotatef(z_rotate, 1, 0, 0)
        else:
            glRotatef(360 - z_rotate, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, int(textures[1]))
    DrawCube(0.2, 1, 0.2)

    glPopMatrix()

#right leg
    glPushMatrix()          
    glTranslatef(0.6, -2.8, 0)
    glRotatef(4 * fly, 1, 0, 0)
    glRotatef(360 - z_rotate, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, int(textures[2]))
    DrawCube(0.4, 1.1, 0.4)
    glTranslatef(0, -2.5, 0)
    glRotatef(360 - 4 * fly, 1, 0, 0)
    if(z_rotate < 180):
        glRotatef(360-z_rotate,1,0,0)
    else:
        glRotatef(z_rotate, 1, 0, 0)
    DrawCube(0.4,1.1,0.4)
    
    if(fly >= .1):
        glTranslatef(0,-3,0)
        #glRotatef(360-20*fly,1,0,0)
        if(fly >= 4):
            glScalef(1.5 + increase * 20, 1.5 + increase * 20, 1.5 + increase * 20)
        glBindTexture(GL_TEXTURE_2D, int(textures[7]))
        gluSphere(quadratic, .5, 64, 64)

        glTranslatef(0,-.8,0)
        glBindTexture(GL_TEXTURE_2D, int(textures[7]))
        if(fly >= 5):
            glScalef(1, 1.5 + increase * 100, 1)
        gluSphere(quadratic, .3, 64, 64)

        glTranslatef(0, -0.4, 0)
        if(fly >= 4):
            glScalef(1, 1.5 + increase * 20, 1)
        gluSphere(quadratic, 0.2, 64, 64)
    
    glPopMatrix()


#left leg
    glPushMatrix()          
    glTranslatef(-0.6,-2.8,0)
    glRotatef(4*fly,1,0,0)
    glRotatef(z_rotate,1,0,0)
    glBindTexture(GL_TEXTURE_2D, int(textures[2]))
    DrawCube(0.4,1.1,0.4)
    glTranslatef(0,-2.5,0)
    glRotatef(360-10*fly,1,0,0)
    if(z_rotate < 180):
        glRotatef(360 - z_rotate, 1, 0, 0)
    else:
        glRotatef(z_rotate, 1, 0, 0)
    DrawCube(0.4, 1.1, 0.4)

    if(fly >=.1):
        glTranslatef(0, -3, 0)
        #glRotatef(360-20*fly,1,0,0)
        glBindTexture(GL_TEXTURE_2D, int(textures[7]))
        if(fly >= 4):
            glScalef(1.5 + increase * 20, 1.5 + increase * 20, 1.5 + increase * 20)
        gluSphere(quadratic, .5, 64, 64)
    
        glTranslatef(0, -0.8, 0)
        glBindTexture(GL_TEXTURE_2D, int(textures[7]))
        if(fly >= 5):
            glScalef(1, 1.5 + increase * 100, 1)
        gluSphere(quadratic, .3, 64, 64)
    
        glTranslatef(0, -0.4, 0)
        if(fly >= 4):
            glScalef(1, 1.5 + increase * 20, 1)
        gluSphere(quadratic, 0.2, 64, 64)
        
    glPopMatrix()
    glutSwapBuffers()


def DrawCube(x, y, z):
    """
    Here we map the vertex of a cube with the texture. Every face of a cube is drawn and with it's vertices a texture is mapped.
    """
    glBegin(GL_QUADS)               
  
  #Cube
    # Front Face (note that the texture's corners have to match the quad's corners)
    glTexCoord2f(0.0, 0.0); glVertex3f(-x, -2 * y,  z)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( x, -2 * y,  z)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( x,  y - y,  z)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-x,  y - y,  z)  # Top Left Of The Texture and Quad
    
    # Back Face
    glTexCoord2f(1.0, 0.0); glVertex3f(-x, -2 * y, -z)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-x,  y - y, -z)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( x,  y - y, -z)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( x, -2 * y, -z)  # Bottom Left Of The Texture and Quad
    
    # Top Face
    glTexCoord2f(0.0, 1.0); glVertex3f(-x,  y - y, -z)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(-x,  y - y,  z)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( x,  y - y,  z)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( x,  y - y, -z)  # Top Right Of The Texture and Quad
    
    # Bottom Face      
    glTexCoord2f(1.0, 1.0); glVertex3f(-x, -2 * y, -z)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( x, -2 * y, -z)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( x, -2 * y,  z)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-x, -2 * y,  z)  # Bottom Right Of The Texture and Quad
    
    # Right face
    glTexCoord2f(1.0, 0.0); glVertex3f( x, -2 * y, -z)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( x,  y - y, -z)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( x,  y - y,  z)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( x, -2 * y,  z)  # Bottom Left Of The Texture and Quad
    
    # Left Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-x, -2 * y, -z)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-x, -2 * y,  z)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-x,  y - y,  z)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-x,  y - y, -z)  # Top Left Of The Texture and Quad
    
    glEnd();

def keyboardFunc(key, x, y):
    """
    All the keys are set here. Here, to take angles in radian PI/180 is multiplied to degrees.
    """
    global object, texture_num, light, x_rotate, y_rotate ,z_rotate, angle, fly , increase ,modeB
    global theta, x_land, z_land, eye
    
    if(z_rotate > 30 and z_rotate < 180):
        angle = -5
    if(z_rotate > 180 and z_rotate < 330):
        angle = 5
    #This is ESCAPE KEY used to exit code.
    if key == '\033': 
        sys.exit()
    elif key == 'a': 
        y_rotate = float((y_rotate - 10) % 360)
    elif key == 'd': 
        y_rotate = float((y_rotate + 10) % 360)
    elif key == 'w': 
        x_rotate = float((x_rotate + 10) % 360)
    elif key == 's': 
        x_rotate = float((x_rotate - 10) % 360)
    elif key == 'c':
        eye = (eye - 10) % 360
    elif key == 'r':
        if(modeB == -1):
            if(fly >= 4.8 ):
                z_rotate = 30
            elif(fly <= 0.1):
                z_rotate = float((z_rotate + angle) % 360)
            if (abs(x_land) < 200 and abs(z_land) < 200):
                z_land = float(z_land + math.cos(((360 - theta)/180) * 3.1416))
                x_land = float(x_land + math.sin(((360 - theta)/180) * 3.1416))
            else:
                if z_land > 0:
                    z_land = float(z_land - abs(math.cos(((360 - theta)/180) * 3.1416)))
                else:
                    z_land = float(z_land + abs(math.cos(((360 - theta)/180) * 3.1416)))
                if x_land > 0:    
                    x_land = float(x_land - abs(math.sin(((360 - theta)/180) * 3.1416)))
                else:
                    x_land = float(x_land + abs(math.sin(((360 - theta)/180) * 3.1416)))
    #This is SPACE Key used to make the humanoid jump in air.
    elif key == '\040':
        if fly < 0.1:
            fly = .1
            increase = 0.1
            z_rotate = 0
            sounds_thrust.play()
        elif(fly >= 5):
            increase = -0.1
            fly = 4.9;
            z_rotate = 0
            sounds_thrust.play()                
    elif key == 'o':
        theta = float((theta - 5) % 360)
    elif key == 'p':
        theta = float((theta + 5) % 360)
    glutPostRedisplay()
    
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)
glutInitWindowPosition(0,0)
glutCreateWindow('MY HUMANOID!')
glutDisplayFunc(display)
glutKeyboardFunc(keyboardFunc)

InitGL(640, 480)
glutMainLoop()