import math
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import opengl_window
from PIL import Image
from loaders import ObjLoader, load_texture


#              positions        texture_coords
cube_buffer = [-0.5, -0.5,  0.5, 0.0, 0.0,
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

             0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5,  0.5, -0.5, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0,
             0.5,  0.5,  0.5, 0.0, 1.0]

cube_buffer = np.array(cube_buffer, dtype=np.float32)

cube_indices = [ 0,  1,  2,  2,  3,  0,
                 4,  5,  6,  6,  7,  4,
                 8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

cube_indices = np.array(cube_indices, dtype=np.uint32)


with opengl_window() as window:
    vertex_src = """
    # version 410

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec2 a_texture;
    layout(location = 2) in vec3 a_offset;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;
    uniform mat4 move;

    out vec2 v_texture;

    void main()
    {
        vec3 final_pos = a_position + a_offset;
        gl_Position =  projection * view * move * model * vec4(final_pos, 1.0f);
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
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    # cube VAO
    glBindVertexArray(VAO)
    # cube Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)
    # cube Element Buffer Object
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)

    # cube vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 5, ctypes.c_void_p(0))
    # cube textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 5, ctypes.c_void_p(12))

    textures = glGenTextures(1)
    load_texture("textures/crate.jpg", textures)

    # instance VBO
    instance_array = []
    offset = 1

    for z in range(0, 100, 2):
        for y in range(0, 100, 2):
            for x in range(0, 100, 2):
                translation = pyrr.Vector3([0.0, 0.0, 0.0])
                translation.x = x + offset
                translation.y = y + offset
                translation.z = z + offset
                instance_array.append(translation)

    len_of_instance_array = len(instance_array) # do this before you flatten the array
    instance_array = np.array(instance_array, np.float32).flatten()

    instanceVBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
    glBufferData(GL_ARRAY_BUFFER, instance_array.nbytes, instance_array, GL_STATIC_DRAW)

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glVertexAttribDivisor(2, 1) # 1 means, every instance will have it's own translate

    program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45,  1280 / 720, 0.1, 100)
    cube_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-50.0, -50.0, -200.0]))

    model_loc = glGetUniformLocation(program, "model")
    proj_loc = glGetUniformLocation(program, "projection")
    view_loc = glGetUniformLocation(program, "view")
    move_loc = glGetUniformLocation(program, "move")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube_pos)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        move = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, glfw.get_time()*8]))
        glUniformMatrix4fv(move_loc, 1, GL_FALSE, move)

        view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glDrawElementsInstanced(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None, len_of_instance_array)

        glfw.swap_buffers(window)

