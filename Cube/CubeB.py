"""
#####################################
## IT 441 Computer Graphics
## Instructor:Nitin Raje
## Implemented By: Shalin Shah
## ID : 201101179
#####################################
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

rotate = 0
ASPECT_RATIO = 1
FIELD_OF_VIEW = 60
Z_NEAR = 0.5
Z_FAR = 20

def display():
	global rotate
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glColor3f (1.0, 1.0, 1.0)
	glLoadIdentity ()             

	gluLookAt (0.0, 0.0, 5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	glRotatef (rotate, 0.0, 1.0, 0.0)
	glutSolidCube (2)
	
	glFlush()

def keyboard(key, x, y):
	global rotate
	if key == chr(27):
		import sys
		sys.exit(0)
	if key == 'r':
		rotate += 5
	glutPostRedisplay()

"""
#This method will clip the outer region of the cube's edges. Here we can clip only 6 edges of the cube since the GL_MAX_CLIP_PLANES = 6 for my graphic card. It is the harware limitation. 
#Incase, more plains were available then we could done that simply by adding two more equations for plain one of which is shown below as PLANE6 (COMMENTED!)
#REFERENCES :- 
#[1]http://www.opengl.org/discussion_boards/showthread.php/168589-getMaxGLPlanes-GL_MAX_CLIP_PLANES-customizable
#[2]http://feedback.wildfiregames.com/report/opengl/device/GeForce%209400 
"""
def clipEdges():
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_CLIP_PLANE0)
	glClipPlane(GL_CLIP_PLANE0,( -1.8, -1.8, -1.8, -1))
	glEnable(GL_CLIP_PLANE1)
	glClipPlane(GL_CLIP_PLANE1,( 1.8, -1.8, -1.8, -1))
	glEnable(GL_CLIP_PLANE2)
	glClipPlane(GL_CLIP_PLANE2,( -1.8, 1.8, -1.8, -1))
	glEnable(GL_CLIP_PLANE3)
	glClipPlane(GL_CLIP_PLANE3,(1, 1, 1, 5.4))
	glEnable(GL_CLIP_PLANE4)
	glClipPlane(GL_CLIP_PLANE4,( -1, 1, 1, 5.4))
	glEnable(GL_CLIP_PLANE5)
	glClipPlane(GL_CLIP_PLANE5,( 1, -1, 1, 5.4))
	#glEnable(GL_CLIP_PLANE6)
	#glClipPlane(GL_CLIP_PLANE5,( 1, 1, -1, 5.4))

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (500, 500)
glutInitWindowPosition (100, 100)
glutCreateWindow ('Clipped Cube')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

glClearColor(0, 0, 0, 0)
glShadeModel(GL_FLAT)
sample = glGetIntegerv(GL_MAX_CLIP_PLANES)
print "No of clipping planes available: ", sample

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(FIELD_OF_VIEW, ASPECT_RATIO, Z_NEAR, Z_FAR)

clipEdges()

glutMainLoop()
