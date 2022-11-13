import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from utils import opengl_window


vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
             0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)

with opengl_window() as window:
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    vertex_src = """
    # version 410

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec3 a_color;

    out vec3 v_color;

    void main()
    {
        gl_Position = vec4(a_position, 1.0);
        v_color = a_color;
    }
    """

    fragment_src = """
    # version 410

    in vec3 v_color;
    out vec4 out_color;

    void main()
    {
        out_color = vec4(v_color, 1.0);
    }
    """
    program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    position = glGetAttribLocation(program, "a_position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    color = glGetAttribLocation(program, "a_color")
    glEnableVertexAttribArray(color)
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glfw.swap_buffers(window)
