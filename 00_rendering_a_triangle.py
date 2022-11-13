import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from utils import opengl_window

"""
Tutorial: https://www.youtube.com/watch?v=bmCYgoCAyMQ&t=517s&ab_channel=AtiByte
"""

"""
Define the vertices to be used
"""
vertices = [
    # vertex 1
    -0.5, 
    -0.5, 
    0.0,
    # color for vertex 1
    1.0,
    0.0,
    0.0,
    # vertex 2
    0.5,
    -0.5,
    0.0,
    # color for vertex 2
    0.0,
    1.0,
    0.0,
    # vertex 3
    0.0,
    0.5,
    0.0,
    # color for vertex 3
    0.0,
    0.0,
    1.0,
]

vertices = np.array(vertices, dtype=np.float32)
with opengl_window() as window:
    """
    #### Setup a vertex buffer object and bind it to the context
    Buffer Objects are OpenGL Objects that store an array of unformatted memory allocated by the OpenGL context (AKA the GPU).
    These can be used to store vertex data, pixel data retrieved from images or the framebuffer, and a variety of other things.

    Generate 1 Vertex Buffer Object on the GPU, only an identifier to the memory is handed out. This is because in the past, 
    GPU, CPU communication was built around a client service architecture and throughput was an issue, as a result the API was
    built around minimizing network throughput as much as possible. Hence, passing the whole
    state around wouldn't make sense, so instead an identifier to the memory is handed out.

    // Generate a name for a new buffer.
    // e.g. buffer = 2
    """
    VBO = glGenBuffers(1)

    """
    Bind the buffer to a certain target (in this case GL_ARRAY_BUFFER) in the context
    the target can be thought of as a global variable in the OpenGL context, and the 
    data in the target will be used in some way (https://docs.gl/gl3/glBindBuffer)

    // Make the new buffer active, creating it if necessary.
    // Kind of like:
    // if (opengl->buffers[buffer] == null)
    //     opengl->buffers[buffer] = new Buffer()
    // opengl->current_array_buffer = opengl->buffers[buffer]

    https://stackoverflow.com/questions/21652546/what-is-the-role-of-glbindvertexarrays-vs-glbindbuffer-and-what-is-their-relatio
    """
    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    """
    Upload vertices data to the GPU. Creates and initializes a buffer object's (GL_ARRAY_BUFFER) data store, this will
    most likely use direct memory access (DMA) to transfer the data from RAM to the GPU

    There are multiple targets in the OpenGL context 
    - GL_ARRAY_BUFFER
    - GL_COPY_READ_BUFFER
    - GL_COPY_WRITE_BUFFER
    - GL_ELEMENT_ARRAY_BUFFER
    - GL_PIXEL_PACK_BUFFER
    - GL_PIXEL_UNPACK_BUFFER
    - GL_TEXTURE_BUFFER
    - GL_TRANSFORM_FEEDBACK_BUFFER
    - GL_UNIFORM_BUFFER
    (https://docs.gl/gl3/glBufferData) 

    // Upload a bunch of data into the active array buffer
    // Kind of like:
    // opengl->current_array_buffer->data = new byte[sizeof(points)]
    // memcpy(opengl->current_array_buffer->data, points, sizeof(points))
    """
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)



    """
    ### Use a Vertex Array Object to give the VBO semantics

    Basically Vertex Array Objects encapsulate vertex array state in OpenGL 3.0. Beginning with OpenGL 3.1
    (in lieu of GL_ARB_compatibility) and OpenGL 3.2+ Core profiles, you must have a non-zero VAO bound at
    all times for commands like glVertexAttribPointer (...) or glDrawArrays (...) to function. 
    The bound VAO forms the necessary context for these commands, and stores the state persistently.

    Most meshes will use a collection of one or more vertex buffer objects to hold vertex points, texture-coordinates, 
    vertex normals, etc.  In older GL implementations we would have to bind each one, and define their memory layout, 
    every time that we draw the mesh.  To simplify that, we have new thing called the vertex array object (VAO), 
    which remembers all of the vertex buffers that you want to use, and the memory layout of each one. We set up
    the vertex array object once per mesh. When we want to draw, all we do then is bind the VAO and draw.
    """

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # """
    # ### Make the buffer the active array buffer.
    # Attach the active buffer to the active array,
    # as an array of vectors with 4 floats each.
    # Kind of like:
    # opengl->current_vertex_array->attributes[attr] = {
    #     type = GL_FLOAT,
    #     size = 4,
    #     data = opengl->current_array_buffer
    # }
    # """
    # glBindBuffer(GL_ARRAY_BUFFER, VBO)

    """
    #### Compile shaders
    There are 5 shader stages: (https://www.khronos.org/opengl/wiki/Shader)
    - Vertex Shaders: `GL_VERTEX_SHADER`
    - Tessellation Control and Evaluation Shaders: `GL_TESS_CONTROL_SHADER` and `GL_TESS_EVALUATION_SHADER`. (requires GL 4.0 or ARB_tessellation_shader)
    - Geometry Shaders: `GL_GEOMETRY_SHADER`
    - Fragment Shaders: `GL_FRAGMENT_SHADER`
    - Compute Shaders: `GL_COMPUTE_SHADER`. (requires GL 4.3 or ARB_compute_shader)

    The compilation of a shader means to compile the shader language, in this case GLSL instead machine code which is specific to GPU with a instruction set architecture
    """

    vertex_src = """
    #version 410 core
    in vec3 a_position;
    in vec3 a_color;
    out vec3 v_color;
    void main()
    {
        gl_Position = vec4(a_position, 1.0);
        v_color = a_color;
    }
    """

    fragment_src = """
    #version 410 core
    in vec3 v_color;
    out vec4 out_color;
    void main()
    {
        out_color = vec4(v_color, 1.0);
    }
    """

    vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)


    """
    #### Compile the program
    compileProgram is a convenience method that will:
    1. Create a new program through `glCreateProgram`
    2. Attach shaders through `glAttachProgram`
    3. Link the program

    A program object can combine multiple shader stages (built from shader objects) into 
    a single, linked whole. A program pipeline object can combine programs 
    that contain individual shader stages into a whole pipeline.
    (https://www.khronos.org/opengl/wiki/GLSL_Object)
    """

    program = compileProgram(vertex_shader, fragment_shader)
    print(f"Program address: {program}")


    """
    #### Give semantics to the buffer data
    When the vertices are updated to the GPU, it's a blob of memory with no semantics. To give 
    semantics to the data to tell the shaders what the data means we have to explicity tell the GPU
    how to interpret the buffer data
    """

    """
    Get the index location of the "a_position" in the shader and allow a separate value to be used for
    each vertex
    (https://stackoverflow.com/questions/39264296/what-is-the-purpose-of-glenablevertexattribarraygluint-index-in-opengl)
    """

    """
    The stride of vertex positions in data bound to GL_ARRAY_BUFFER target represented by VBO
    The vertices array is:
    [point 1 for vertex 1,
    point 2 for vertex 1,
    point 3 for vertex 1,
    color 1 for vertex 1,
    color 2 for vertex 1,
    color 3 for vertex 1,
    ...
    ]

    Each point/color is fp32 so 4 bytes of memory. The stride is the byte offset between consecutive
    generic vertex attributes. Therefore a stride of 24 bytes is needed between the data representing
    the vertex data (12 bytes for the vertex, 12 bytes for the color)
    """
    STRIDE = 24
    OFFSET = 12

    position = glGetAttribLocation(program, "a_position")
    print(f"Position address: {position}")

    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, STRIDE, ctypes.c_void_p(0))

    color = glGetAttribLocation(program, "a_color")
    print(f"Color address: {color}")

    glEnableVertexAttribArray(color)
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, STRIDE, ctypes.c_void_p(0 + OFFSET))


    glUseProgram(program)
    glClearColor(0, 0.1, 0.1, 1)

    """
    #### Render the triangle
    """

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        glfw.swap_buffers(window)