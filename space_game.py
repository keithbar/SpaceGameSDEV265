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

from entities import Enemy, enemy_list, Obstacle, obstacle_list, \
    Collectable, collectable_list, Bullet, bullet_list
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Constants

# Values concerning the window, including default dimensions.
WINDOW_TITLE = "SDEV 265 Space Game"
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 720
        
# Class for the main game loop, extends Arcade's Window class
class SpaceGame(arcade.Window):
    def __init__(self):
        # Initialize the window
        super().__init__(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_TITLE, resizable=True)

        # The background is set to gray for testing purposes, to
        # ensure the letterboxing works correctly when resizing
        arcade.set_background_color(arcade.color.GRAY)

        # Populate array of Enemies for testing purposes
        for _ in range(5):
            enemy_list.append(Enemy(0))

        # Populate array of Obstacles for testing purposes
        for _ in range(5):
            obstacle_list.append(Obstacle(0))

        # Populate array of Collectables for testing purposes
        for _ in range(5):
            collectable_list.append(Collectable(0))

        # Populate array of Bullets for testing purposes
        for _ in range(5):
            bullet_list.append(Bullet(0))
        
    # Drawing method that is called on every frame
    def on_draw(self):
        # Start by clearing the previous frame
        self.clear()

        # Now update and draw all the entities
        for enemy in enemy_list:
            enemy.update()
            enemy.draw()
        for obstacle in obstacle_list:
            obstacle.update()
            obstacle.draw()
        for collectable in collectable_list:
            collectable.update()
            collectable.draw()
        for bullet in bullet_list:
            bullet.update()
            bullet.draw()

        # Remove off screen and dead entities
        enemy_list[:] = list(filter(lambda enemy: enemy.y > -10 and enemy.health > 0, enemy_list))
        obstacle_list[:] = list(filter(lambda obstacle: obstacle.y > -10 and obstacle.health > 0, obstacle_list))
        collectable_list[:] = list(filter(lambda collectable: collectable.y > -10, collectable_list))
        bullet_list[:] = list(filter(lambda bullet: bullet.y < SCREEN_HEIGHT + 10 and bullet.y > -10, bullet_list))

        # Print debug info
        arcade.draw_text("Enemy count: " + str(len(enemy_list)), 50, 90, arcade.color.BLACK)
        arcade.draw_text("Obstacle count: " + str(len(obstacle_list)), 50, 70, arcade.color.BLACK)
        arcade.draw_text("Collectable count: " + str(len(collectable_list)), 50, 50, arcade.color.BLACK)
        arcade.draw_text("Bullet count: " + str(len(bullet_list)), 50, 30, arcade.color.BLACK)

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