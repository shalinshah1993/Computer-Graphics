"""
#####################################
## IT 441 Computer Graphics
## Instructor:Nitin Raje
## Implemented By: Shalin Shah
## ID : 201101179
#####################################
"""

import sys
from PIL import Image
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *	

rotate = 0.0
MATERIAL_SHINENESS = [8.0]
MATERIAL_SPECULAR_CONTENT = [1.0, 1.0, 1.0, 1.0]
LIGHT_POSITION = [ 3.0, 3.0, 0.0, 0.0]

def sphere():
	"""
	Vector on a 3D sphere has coordinates - (r * Cos(theta) * Sin(phi), r * Sin(theta) * Sin(phi), r * Cos(phi))
	phi - Angle made by the vector with Z axis
	theta - Angle made by the vector projected in X-Y plane with X axis.
	"""
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glShadeModel(GL_SMOOTH)
	glMatrixMode(GL_MODELVIEW)

	glLoadIdentity()
	gluLookAt(-3, 1, 0, 0, 0, 0, 0, 1, 0)
	glColor3d(0, 0, 0)
	glRotatef(rotate, 1.0, 1.0, 1.0)    
	glColor3f(1.0, 1.0, 0.0)
	
	glBegin(GL_QUAD_STRIP)
	for theta in xrange(0, 180, 2):
		for phi in xrange(0, 360, 10):            
			x = cos(theta * pi/180) * sin(phi * pi/180)
			y = sin(theta * pi/180) * sin(phi * pi/180)
			z = cos(phi * pi/180)
			glVertex3d(x, y, z)
	glEnd()    
	glFlush()
    
def keys(key, x, y):
	"""
	This function is used to take user input from keyboard.
	"""
	global rotate

	if key == 'q' or key == 'Q': 
		sys.exit(0)
	elif key == 'r' or key == 'R': 
		rotate = (rotate + 5) % 360

	glutPostRedisplay()
   
if __name__ == "__main__":
	#Set basic parameters of Frame
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)
	glutInitWindowPosition(100, 100)
	glutCreateWindow("Sphere without gluWireSphere")
	glutDisplayFunc(sphere)
	glutKeyboardFunc(keys)

	#Set clear color to white. 30 deg is FOV and aspect ratio is 1.
	glClearColor(0, 0, 0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60, 1, 0.5, 100.0)

	#Set the lightning mode on and then enable lights.
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_COLOR_MATERIAL)     
	glEnable(GL_DEPTH_TEST)

	glShadeModel(GL_SMOOTH)                           
	glMaterialfv(GL_FRONT, GL_SPECULAR, MATERIAL_SPECULAR_CONTENT)   
	glMaterialfv(GL_FRONT, GL_SHININESS, MATERIAL_SHINENESS) 
	glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)   
	glColorMaterial(GL_FRONT, GL_DIFFUSE)

	glutMainLoop()
