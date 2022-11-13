import math
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import opengl_window
from PIL import Image


vertices = [-0.5, -0.5,  0.5, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 1.0,
            -0.5,  0.5, -0.5, 0.0, 1.0,

             0.5, -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0,

            -0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0,

             0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5,  0.5, 1.0, 1.0,
             0.5, 0.5,  0.5, 0.0, 1.0]

indices = [ 0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9, 10, 10, 11,  8,
           12, 13, 14, 14, 15, 12,
           16, 17, 18, 18, 19, 16,
           20, 21, 22, 22, 23, 20]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

with opengl_window() as window:
    vertex_src = """
    # version 410

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec2 a_texture;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;

    out vec3 v_color;
    out vec2 v_texture;

    void main()
    {
        gl_Position = projection * view * model * vec4(a_position, 1.0);
        v_texture = a_texture;
    }
    """

    fragment_src = """
    # version 410

    in vec2 v_texture;

    out vec4 out_color;

    uniform sampler2D s_texture;

    void main()
    {
        out_color = texture(s_texture, v_texture);
    }
    """

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    position = glGetAttribLocation(program, "a_position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))


    texture = glGetAttribLocation(program, "a_texture")
    glEnableVertexAttribArray(texture)
    glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    image = Image.open("textures/crate.jpg")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    # img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280/720, 0.1, 100)
    translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1, 0, 0]))


    model_loc = glGetUniformLocation(program, "model")
    proj_loc = glGetUniformLocation(program, "projection")
    view_loc = glGetUniformLocation(program, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, translation)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # the main application loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camX = math.sin(glfw.get_time()) * 10
        camZ = math.cos(glfw.get_time()) * 10

        # eye, target, up
        view = pyrr.matrix44.create_look_at(pyrr.Vector3([camX, 5.0, camZ]), pyrr.Vector3([0.0, 0.0, 0.0]),
                                            pyrr.Vector3([0.0, 1.0, 0.0]))

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)