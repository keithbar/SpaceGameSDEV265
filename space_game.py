import arcade
import random

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

# Enemy types and their stats
ENEMY_STATS = {
    "basic_straight": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_zigzag": { "health": 1, "velocity_x": (1, 3), "velocity_y": (-3, -1) },
    "basic_wave": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_wait": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_fast": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_dodge": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
}

# Obstacle types and their defaul stats
OBSTACLE_STATS = {
    "small":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "small_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "medium":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "medium_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "large":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "large_fast":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "long":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) },
    "long_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), "velocity_rotation": (-5, 5) }
}

# Collectable types and their stats
COLLECTABLE_STATS = {
    "attack_up": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "attack_down": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "defense_up": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "defense_down": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "health_small": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "health_large": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "speed_up": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "speed_down": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "fire_rate_up": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "fire_rate_down": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "bullet_speed_up": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "bullet_speed_down": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "destroy_all_enemies": { "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "invincible": { "velocity_x": (0, 0), "velocity_y": (-3, -1) }
}

playerSpeed = 5
bulletSpeed = 7
        
# Class for the main game loop, extends Arcade's Window class
class SpaceGame(arcade.Window):
    def __init__(self):
        # Initialize the window
        super().__init__(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_TITLE, resizable=True)
        self.player = None
        self.player_list = None
        self.bullet_list = None
        self.obstacle_list = None
        self.collectable_list = None
        
        #This is for the enemies when implamented 
        self.enemy_list = None
        self.enemy_direction = 1
        
        #initializes our score and sets us up to implament the game over when you lose and add new waves in the future
        self.score = 0  
        self.game_over = False  
        self.wave = 1  

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.collectable_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.score = 0  
        self.game_over = False  
        self.wave = 1  
         
        # This is our player I tried to find different sprites but this is what I have for now 
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.8)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 50
        self.player.health = 100
        self.player_list.append(self.player)

        # Spawns some objects for testing purposes
        for _ in range(5):
            self.spawn_enemy("basic_straight")
            self.spawn_obstacle("small")
            self.spawn_collectable("health_small")
        
    # Drawing method that is called on every frame
    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.obstacle_list.draw()
        self.collectable_list.draw()
        
        # This will display the score and text for our game
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Wave: {self.wave}", SCREEN_WIDTH - 130, SCREEN_HEIGHT - 50, arcade.color.WHITE, 20)

        # Debug info
        arcade.draw_text(f"Health: {self.player.health}", 10, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -playerSpeed

        elif key == arcade.key.RIGHT:
            self.player.change_x = playerSpeed

        elif key == arcade.key.UP:
            self.player.change_y = playerSpeed

        elif key == arcade.key.DOWN:
            self.player.change_y = -playerSpeed
        
        #This is the projectile I found that looked the best so far however we can change for whatever everyone likes 
        elif key == arcade.key.SPACE:
            bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 0.8)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y + 20
            bullet.change_y = bulletSpeed
            self.bullet_list.append(bullet)

    def update(self, delta_time):
        if self.game_over:
            return  

        self.player_list.update()
        self.bullet_list.update()
        self.enemy_list.update()
        self.obstacle_list.update()
        self.collectable_list.update()

        # This is what keeps our ship confined to our screen
        if self.player.left < 0:
            self.player.left = 0

        elif self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        if self.player.bottom < 0:
            self.player.bottom = 0

        elif self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT

        # Removes the bullets that are off screen 
        for bullet in self.bullet_list:
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Removes enemies that are off screen
        for enemy in self.enemy_list:
            if enemy.top < 0:
                enemy.remove_from_sprite_lists()

        # Removes obstacles that are off screen
        for obstacle in self.obstacle_list:
            if obstacle.top < 0:
                obstacle.remove_from_sprite_lists()

        # Removes collectables that are off screen
        for collectable in self.collectable_list:
            if collectable.top < 0:
                collectable.remove_from_sprite_lists()

        # Check for collision
        for player in self.player_list:
            player_enemy_collision = arcade.check_for_collision_with_list(
                player, self.enemy_list
            )
            for enemy in player_enemy_collision:
                player.health -= enemy.strength
                enemy.remove_from_sprite_lists()
    
    #Updates button press on release so that we dont continue moving
    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
        elif key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0

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

    # Spawns a new enemy of the given type (see ENEMY_STATS above)
    def spawn_enemy(self, type):
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png", 0.8, flipped_vertically=True)
        enemy.center_x = random.uniform(0, SCREEN_WIDTH)
        enemy.center_y = SCREEN_HEIGHT + enemy.height
        enemy.change_x = random.uniform(*ENEMY_STATS[type]["velocity_x"])
        enemy.change_y = random.uniform(*ENEMY_STATS[type]["velocity_y"])
        enemy.type = type
        enemy.health = ENEMY_STATS[type]["health"]
        enemy.strength = 1 # Dictates how much damage this enemy does when colliding with player
        self.enemy_list.append(enemy)

    # Spawns a new obstacle of the given type (see OBSTACLE_STATS above)
    def spawn_obstacle(self, type):
        obstacle = arcade.Sprite(":resources:images/space_shooter/meteorGrey_small2.png")
        obstacle.center_x = random.uniform(0, SCREEN_WIDTH)
        obstacle.center_y = SCREEN_HEIGHT + obstacle.height
        obstacle.change_x = random.uniform(*OBSTACLE_STATS[type]["velocity_x"])
        obstacle.change_y = random.uniform(*OBSTACLE_STATS[type]["velocity_y"])
        obstacle.change_angle = random.uniform(*OBSTACLE_STATS[type]["velocity_rotation"])
        obstacle.type = type
        obstacle.health = OBSTACLE_STATS[type]["health"]
        self.obstacle_list.append(obstacle)

    # Spawns a new collectable of the given type (see COLLECTABLE_STATS above)
    def spawn_collectable(self, type):
        collectable = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
        collectable.center_x = random.uniform(0, SCREEN_WIDTH)
        collectable.center_y = SCREEN_HEIGHT + collectable.height
        collectable.change_x = random.uniform(*COLLECTABLE_STATS[type]["velocity_x"])
        collectable.change_y = random.uniform(*COLLECTABLE_STATS[type]["velocity_y"])
        collectable.type = type
        self.collectable_list.append(collectable)

def main():
    game = SpaceGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()