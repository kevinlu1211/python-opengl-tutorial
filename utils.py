import glfw
import numpy as np
from OpenGL.GL import *
from camera import Camera

from contextlib import contextmanager

lastX, lastY = 0 , 0
first_mouse = True
left, right, forward, backward = False, False, False, False

@contextmanager
def opengl_window(window_width=1280, window_height=720, window_pos_x=640, window_pos_y=360):
    try:
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        window = glfw.create_window(window_width, window_height, "My OpenGL window", None, None)

        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
    
        cam = Camera()
        global lastX, lastY
        lastX =  window_width / 2
        lastY = window_height / 2

        # the keyboard input callback
        def key_input_clb(window, key, scancode, action, mode):
            global left, right, forward, backward
            if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
                glfw.set_window_should_close(window, True)

            if key == glfw.KEY_W and action == glfw.PRESS:
                forward = True
            elif key == glfw.KEY_W and action == glfw.RELEASE:
                forward = False
            if key == glfw.KEY_S and action == glfw.PRESS:
                backward = True
            elif key == glfw.KEY_S and action == glfw.RELEASE:
                backward = False
            if key == glfw.KEY_A and action == glfw.PRESS:
                left = True
            elif key == glfw.KEY_A and action == glfw.RELEASE:
                left = False
            if key == glfw.KEY_D and action == glfw.PRESS:
                right = True
            elif key == glfw.KEY_D and action == glfw.RELEASE:
                right = False

        # do the movement, call this function in the main loop
        def do_movement():
            if left:
                cam.process_keyboard("LEFT", 0.1)
            if right:
                cam.process_keyboard("RIGHT", 0.1)
            if forward:
                cam.process_keyboard("FORWARD", 0.1)
            if backward:
                cam.process_keyboard("BACKWARD", 0.1)


        # the mouse position callback function
        def mouse_look_clb(window, xpos, ypos):
            global first_mouse, lastX, lastY

            if first_mouse:
                lastX = xpos
                lastY = ypos
                first_mouse = False

            xoffset = xpos - lastX
            yoffset = lastY - ypos

            lastX = xpos
            lastY = ypos

            cam.process_mouse_movement(xoffset, yoffset)

        def window_resize(window, width, height):
            glViewport(0, 0, width, height)
            projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


        # set window's position
        glfw.set_window_pos(window, window_pos_x, window_pos_y)

        # set the callback function for window resize
        glfw.set_window_size_callback(window, window_resize)

        # set the mouse position callback
        glfw.set_cursor_pos_callback(window, mouse_look_clb)

        # set the keyboard input callback
        glfw.set_key_callback(window, key_input_clb)

        # capture the mouse cursor
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # make the context current
        glfw.make_context_current(window)

        yield window, cam, do_movement
    finally:
        glfw.terminate()
