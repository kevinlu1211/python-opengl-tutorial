import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from utils import opengl_window
from PIL import Image



vertices = [ # position        # color         # texture coordinates
            -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

# Using the texture coordinates above, we will not be able to see
# any effects for the filtering as the UV coordinates of the textures
# range from 0-1. If we use the texture coordinates below, we will
# be able to see the effects of the filtering.
vertices = [ # position        # color         # texture coordinates
            -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  -1.0, 2.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  -1.0, 2.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  -1.0, 2.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  -1.0, 2.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  -1.0, 2.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  -1.0, -1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  2.0, -1.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  2.0, 2.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  -1.0, 2.0]

indices = [0,  1,  2,  2,  3,  0,
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
    layout(location = 1) in vec3 a_color;
    layout(location = 2) in vec2 a_texture;

    uniform mat4 rotation;

    out vec3 v_color;
    out vec2 v_texture;

    void main()
    {
        gl_Position = rotation * vec4(a_position, 1.0);
        v_color = a_color;
        v_texture = a_texture;
        
        //v_texture = 1 - a_texture;                      // Flips the texture vertically and horizontally
        //v_texture = vec2(a_texture.s, 1 - a_texture.t); // Flips the texture vertically
    }
    """

    fragment_src = """
    # version 410

    in vec3 v_color;
    in vec2 v_texture;

    out vec4 out_color;

    uniform sampler2D s_texture;

    void main()
    {
        out_color = texture(s_texture, v_texture);
        // out_color = vec4(v_color, 1.0f);
        // out_color = texture(s_texture, v_texture) * vec4(v_color, 1.0f);
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
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))

    color = glGetAttribLocation(program, "a_color")
    glEnableVertexAttribArray(color)
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))

    texture = glGetAttribLocation(program, "a_texture")
    glEnableVertexAttribArray(texture)
    glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(24))

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # UV & ST coordinates
    # https://stackoverflow.com/questions/10568390/difference-between-uv-and-st-texture-coordinates#:~:text=uv%20coordinates%20start%20from%20the,%2Daxis%20is%20facing%20up).

    # Texture wrapping (addressing) and filtering 
    # https://www.youtube.com/watch?v=DuQDx0ZIxa8&ab_channel=FloatyMonkey

    # Set the texture wrapping (addressing) parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    image = Image.open("textures/cat.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    # Move the image data into the texture for OpenGL to use
    # https://stackoverflow.com/questions/26499361/opengl-what-does-glteximage2d-do
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    rotation_loc = glGetUniformLocation(program, "rotation")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)
    
