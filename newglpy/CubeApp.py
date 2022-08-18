from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math

vertices = (
            ( 1,-1,-1),
            ( 1, 1,-1),
            (-1, 1,-1),
            (-1,-1,-1),
            ( 1,-1, 1),
            ( 1, 1, 1),
            (-1,-1, 1),
            (-1, 1, 1),
            )

faces = (
    (0,1,2),
    (0,2,3),
    (3,2,7),
    (3,6,7),
    (6,7,5),
    (6,5,4),
    (4,5,1),
    (4,1,0),
    (1,5,7),
    (1,7,2),
    (4,0,3),
    (4,3,6)
    )

cores = ( (1,0,0),(1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1),(0.5,1,1),(1,0,0.5) )

class CubeApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Cubo")
        self.size(800,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimplePipeline")
        GL.glUseProgram(self.pipeline)
        self.a = 0
        self.cubeArrayBufferId = None

    def drawCube(self):
        if self.cubeArrayBufferId == None:
            position = array('f')
            color = array('f')
            for f in faces:
                for v in f:
                    position.append(vertices[v][0])
                    position.append(vertices[v][1])
                    position.append(vertices[v][2])
                    color.append(cores[v][0])
                    color.append(cores[v][1]) 
                    color.append(cores[v][2])  
            

            self.cubeArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.cubeArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(color)*color.itemsize, ctypes.c_void_p(color.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        GL.glBindVertexArray(self.cubeArrayBufferId)
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,5),glm.vec3(0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(0,0,1)) * glm.rotate(self.a,glm.vec3(0,1,0)) * glm.rotate(self.a,glm.vec3(1,0,0)) 
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,36)
        self.a += 0.01

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        # Draw a Dotted Cube
        self.drawCube()

CubeApp()
