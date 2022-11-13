import math
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import opengl_window
from PIL import Image
from loaders import ObjLoader, load_texture


chibi_indices, chibi_buffer = ObjLoader.load_model("meshes/chibi.obj")
monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/monkey.obj")

with opengl_window() as window:
    vertex_src = """
    # version 410

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec2 a_texture;
    layout(location = 2) in vec3 a_normal;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;

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

    VAO = glGenVertexArrays(2)
    VBO = glGenBuffers(2)


    # Chibi VAO
    glBindVertexArray(VAO[0])

    # Chibi Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, chibi_buffer.nbytes, chibi_buffer, GL_STATIC_DRAW)

    # Monkey VAO
    glBindVertexArray(VAO[1])
    # Monkey Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)


    program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    textures = glGenTextures(2)
    # chibi vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(0))
    # chibi textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(12))
    # chibi normals
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(20))

    load_texture("meshes/chibi.png", textures[0])


    # monkey vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))
    # monkey textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))
    # monkey normals
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
    load_texture("meshes/monkey.jpg", textures[1])



    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
    chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, 0]))

    # eye, target, up
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

    model_loc = glGetUniformLocation(program, "model")
    proj_loc = glGetUniformLocation(program, "projection")
    view_loc = glGetUniformLocation(program, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # the main application loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        model = pyrr.matrix44.multiply(rot_y, chibi_pos)

        # draw the chibi character
        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(chibi_indices))

        rot_y = pyrr.Matrix44.from_y_rotation(-0.8 * glfw.get_time())
        model = pyrr.matrix44.multiply(rot_y, monkey_pos)

        # draw the monkey head
        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))

        glfw.swap_buffers(window)

        # https://stackoverflow.com/questions/154730/capturing-video-out-of-an-opengl-window-in-windows
        # https://www.glfw.org/docs/latest/context.html#context_offscreen
