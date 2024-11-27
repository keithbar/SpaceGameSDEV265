# Here is an updated skeleton that we can build on for creating the
# game. I've rewritten the game loop to use Python Arcade. It
# currently creates an array of generic entities, each of which is
# displayed on screen as a simple red square.
#
# Next steps might be to implement different classes that extend the
# Entity class, figure out an efficient way to determine when two
# Entities are touching, implement functions to create new Entities,
# implement methods for the different Entity types that determine how
# they behave, etc.

import arcade

# Constants

# These values represent the size of the internal canvas. This is
# the number of pixels that will be computed, which will then be
# scaled to the size of the window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Values concerning the window, including default dimensions.
WINDOW_TITLE = "SDEV 265 Space Game"
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 720

class Entity:
    def __init__(self, x, y, velocityX, velocityY):
        self.x = x
        self.y = y
        self.velocityX = velocityX
        self.velocityY = velocityY

    def update(self):
        self.x += self.velocityX
        self.y += self.velocityY

    def draw(self):
        # Draw a red square on screen. This method can be overridden
        # when making new entity types to draw different shapes,
        # sprites, and/or effects
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.RED_BROWN, 0)

    # Debug function that prints entity information to console. Currently unused.
    def print(self, id):
        print("Entity " + str(id) + " at (" + str(self.x) + ", " + str(self.y) + \
            ") with velocity (" + str(self.velocityX) + ", " + str(self.velocityY) + ")")
        
# Class for the main game loop, extends Arcade's Window class
class SpaceGame(arcade.Window):
    def __init__(self):
        # Initialize the window
        super().__init__(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_TITLE, resizable=True)

        # The background is set to gray for testing purposes, to
        # ensure the letterboxing works correctly when resizing
        arcade.set_background_color(arcade.color.GRAY)

        # Create an array of Entities for testing purposes
        self.entityList = []
        self.entityList.append(Entity(525, 525, .1, -.1))
        self.entityList.append(Entity(523, 544, .5, .4))
        self.entityList.append(Entity(500, 578, .3, -.1))
        self.entityList.append(Entity(545, 554, -.3, .1))
        self.entityList.append(Entity(577, 577, -.1, .1))
        
    # Drawing method that is called on every frame
    def on_draw(self):
        # Start by clearing the previous frame
        self.clear()

        # Now update and draw all the entities
        for entity in self.entityList:
            entity.update()
            entity.draw()

    # Scale the image to the size of the window, maintaining aspect ratio.
    # There may be a simpler way to achieve this result using Arcade's
    # Camera class, but I wasn't able to figure it out.
    # Confusingly, this method refers to two different "viewports" that
    # serve different purposes:
    # 1. The window viewport describes what part of the internal coordinates
    #    will be drawn to the window. We want to keep this consistent so
    #    that the same visuals will be drawn regardless of window size.
    # 2. The context viewport is part of a "context" object that is part of
    #    every Arcade window object, which seems to contain information that
    #    the window uses for rendering. Here we manipulate the context
    #    viewport to change where within the window we draw. This is done to
    #    maintain the image aspect ratio as the user resizes the window.
    def on_resize(self, width, height):
        # Set window viewport; this ensures that the entire screen will be drawn within the window
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        screen_aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
        window_aspect_ratio = width / height

        # Adjusting the window's context viewport allows us to move where within the window we draw
        # This allows us to maintain the image aspect ratio as the window is resized
        if(screen_aspect_ratio >= window_aspect_ratio):
            viewport_width = width
            viewport_height = width / screen_aspect_ratio
            self.ctx.viewport = 0, (height - viewport_height) / 2, viewport_width, viewport_height
        else:
            viewport_width = height * screen_aspect_ratio
            viewport_height = height
            self.ctx.viewport = (width - viewport_width) / 2, 0, viewport_width, viewport_height

def main():
    SpaceGame()
    arcade.run()

if __name__ == "__main__":
    main()