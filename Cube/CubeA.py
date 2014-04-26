"""
#####################################
## IT 441 Computer Graphics
## Instructor:Nitin Raje
## Implemented By: Shalin Shah
## ID : 201101179
#####################################
"""

import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


ROTATE = 0.0
LENGTH = 1.0
VALUE = 0.25

def drawFace():
	"""
	This is the main data structure associated with the in draing the polyhedra. Here, each and every face is associated with it's vertices and six 
	such faces are drawn. This means that MAPPING : FACE -> VERTICES
	"""
	glPushMatrix()
	glTranslatef(-0.5,-0.5,0)
	glBegin(GL_LINE_LOOP)
	
	glVertex3f(0,VALUE,0)
	glVertex3f(VALUE,0,0)
	
	glVertex3f(LENGTH-VALUE,0,0)
	glVertex3f(LENGTH,VALUE,0)
	
	glVertex3f(LENGTH,LENGTH-VALUE,0)
	glVertex3f(LENGTH-VALUE,LENGTH,0)
	
	glVertex3f(VALUE,LENGTH,0)
	glVertex3f(0,LENGTH-VALUE,0)
	
	glEnd()
	glPopMatrix()


def display():
	"""
	This is the display function where in using the drawFace datastructure we construct the polyhedra. Also, we can rotate our polyhedra to have 
	a look at it from different angles.
	"""
	global ROTATE
	glClear(GL_COLOR_BUFFER_BIT)

	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

	glRotatef(ROTATE, 0.0, 1.0, 0.0)
	glPushMatrix()
	glTranslatef(0,0,0.5)
	drawFace()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0,0.5,0)
	glRotatef(90,1,0,0)
	drawFace()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0,-0.5,0)
	glRotatef(90,1,0,0)
	drawFace()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0.5,0,0)
	glRotatef(90,0,1,0)
	drawFace()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(-0.5,0,0)
	glRotatef(90,0,1,0)
	drawFace()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0,0,-0.5)
	drawFace()
	glPopMatrix()

	glFlush()


def keyboard(key, x, y):
	"""
	This function is used to take user input from keyboard.
	"""
	global ROTATE

	if key == chr(27): 
		sys.exit(0)
	elif key == 'r': 
		ROTATE = (ROTATE + 5) % 360
	elif key == 'R': 
		ROTATE = (ROTATE - 5) % 360

	glutPostRedisplay()


if __name__ == '__main__':
	#Set basic parameters of Frame
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(640, 600)
	glutInitWindowPosition(100, 100)
	glutCreateWindow("Truncated Cube!")
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)

	#Set clear color to white. 30 deg is FOV and aspect ratio is width/height.
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity ()
	gluPerspective(60, 640/480, 1.0, 20.0)
		
	glutMainLoop()
