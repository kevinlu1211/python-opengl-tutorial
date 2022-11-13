import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import opengl_window



vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)


with opengl_window() as window:
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)


    vertex_src = """
    # version 410

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec3 a_color;

    uniform mat4 rotation;
    out vec3 v_color;

    void main()
    {
        gl_Position = rotation * vec4(a_position, 1.0);
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
    glEnable(GL_DEPTH_TEST)

    rotation_loc = glGetUniformLocation(program, "rotation")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

        # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x * rot_y)
        # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y)
        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glfw.swap_buffers(window)
    
