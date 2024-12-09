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
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 1 },
    "small_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 1 },
    "medium":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5,), "strength": 2 },
    "medium_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 2 },
    "large":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 3 },
    "large_fast":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 3 },
    "long":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 2 },
    "long_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 2 }
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

# Bullet types and their stats
BULLET_STATS = {
    "player_basic": { "velocity_x": (0, 0), "velocity_y": (bulletSpeed, bulletSpeed), "friendly": True},
    "enemy_basic": { "velocity_x": (0, 0), "velocity_y": (-3, -1), "friendly": False}
}

# An Arcade Window that will be set to display one of the following Views:
# SpaceGameView: The main gameplay
# TitleView: The title screen
# GameOverView: The game over screen
class SpaceGameWindow(arcade.Window):
    def __init__(self):
        # Initialize the window
        super().__init__(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, WINDOW_TITLE, resizable=True)

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
        
# Class for the main game loop, extends Arcade's View class
class SpaceGameView(arcade.View):
    def __init__(self):
        super().__init__()
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
        self.player.health = 1
        self.player_list.append(self.player)

        # Spawns some objects for testing purposes
        for _ in range(5):
            self.spawn_enemy("basic_straight")
            self.spawn_obstacle("small")
            self.spawn_collectable("health_small")
        self.spawn_bullet("enemy_basic", 1000, 1080)
        
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
            self.spawn_bullet("player_basic", self.player.center_x, self.player.center_y + 20)

    def update(self, delta_time):
        if self.player.health <= 0:
            game_over = GameOverView()
            game_over.setup(self.score)
            self.window.show_view(game_over)
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

        # Remove entities that have moved off screen
        self.cull_off_screen()

        # Check for collision between entities
        self.check_collision()
    
    #Updates button press on release so that we dont continue moving
    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
        elif key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0

    def cull_off_screen(self):
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

    #
    def check_collision(self):
        for player in self.player_list:

            # Check for player-enemy collisions
            player_enemy_collision = arcade.check_for_collision_with_list(
                player, self.enemy_list
            )
            # Decrement player health and destroy enemy
            for enemy in player_enemy_collision:
                player.health -= enemy.strength
                enemy.remove_from_sprite_lists()

            # Check for player-bullet collisions
            player_bullet_collision = arcade.check_for_collision_with_list(
                player, self.bullet_list
            )
            for bullet in player_bullet_collision:
                if bullet.friendly == False:
                    player.health -= bullet.strength
                    bullet.remove_from_sprite_lists()

            # Check for player-obstacle collisions
            player_obstacle_collision = arcade.check_for_collision_with_list(
                player, self.obstacle_list
            )
            for obstacle in player_obstacle_collision:
                player.health -= obstacle.strength
                obstacle.remove_from_sprite_lists()

            # Check for player-collectable collisions
            player_collectable_collision = arcade.check_for_collision_with_list(
                player, self.collectable_list
            )
            for collectable in player_collectable_collision:
                self.collect_collectable(player, collectable.type)
                collectable.remove_from_sprite_lists()

        # Check for enemy-bullet collisions
        for bullet in self.bullet_list:
            if bullet.friendly == True:
                enemy_bullet_collision = arcade.check_for_collision_with_list(
                    bullet, self.enemy_list
                )
                for enemy in enemy_bullet_collision:
                    # Update this for enemy health, currently just instakills
                    enemy.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()
                    break

        # Check for obstacle-bullet collisions
        for bullet in self.bullet_list:
            if bullet.friendly == True:
                obstacle_bullet_collision = arcade.check_for_collision_with_list(
                    bullet, self.obstacle_list
                )
                for obstacle in obstacle_bullet_collision:
                    # Update this for obstacle health, currently just instakills
                    obstacle.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()
                    break

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
        obstacle.strength = OBSTACLE_STATS[type]["strength"]
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

    # Spawns a new bullet of the given type (see BULLET_STATS above)
    def spawn_bullet(self, type, x, y):
        bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 0.8)
        bullet.center_x = x
        bullet.center_y = y
        bullet.change_x = random.uniform(*BULLET_STATS[type]["velocity_x"])
        bullet.change_y = random.uniform(*BULLET_STATS[type]["velocity_y"])
        bullet.friendly = BULLET_STATS[type]["friendly"]
        bullet.strength = 1
        self.bullet_list.append(bullet)

    # Applies collectable effects to given player
    def collect_collectable(self, player, type):
        if type == "health_small":
            player.health += 1

START_GAME = 0
HIGH_SCORE = 1
SETTINGS = 2
QUIT_GAME = 3

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_action = START_GAME

    # setup is currently redundant, left it here in case we want to
    # do more with it in the future
    def setup(self):
        self.selected_action = START_GAME

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("SDEV 265\nSPACE GAME", 0, SCREEN_HEIGHT * 0.7,
            font_size = 50, width = SCREEN_WIDTH, align = "center")
        
        # Values to make changing text layout easier
        option_font_size = 25
        option_line_height = 35
        option_y_start = SCREEN_HEIGHT * 0.4

        text_start_game = arcade.Text(" Start Game ", 0, option_y_start, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center")
        text_start_game.draw()

        text_high_score = arcade.Text(" High Scores ", 0, option_y_start - option_line_height, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center")
        text_high_score.draw()

        text_settings = arcade.Text(" Settings ", 0, option_y_start - option_line_height * 2, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center")
        text_settings.draw()

        text_quit = arcade.Text(" Quit ", 0, option_y_start - option_line_height * 3, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center")
        text_quit.draw()
        
        if self.selected_action == START_GAME:
            selected_text = text_start_game
        elif self.selected_action == HIGH_SCORE:
            selected_text = text_high_score
        elif self.selected_action == SETTINGS:
            selected_text = text_settings
        else:
            selected_text = text_quit

        arrow_size = 25
        text_width = selected_text.content_width
        arrow_left_x = SCREEN_WIDTH / 2 - text_width / 2 - arrow_size
        arrow_right_x = SCREEN_WIDTH / 2 + text_width / 2 + arrow_size
        arrow_y = selected_text.y
        arcade.draw_triangle_filled(
            arrow_left_x, arrow_y, 
            arrow_left_x, arrow_y + arrow_size,
            arrow_left_x + arrow_size, arrow_y + arrow_size / 2,
            arcade.color.WHITE
        )
        arcade.draw_triangle_filled(
            arrow_right_x, arrow_y,
            arrow_right_x, arrow_y + arrow_size,
            arrow_right_x - arrow_size, arrow_y + arrow_size / 2,
            arcade.color.WHITE
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.selected_action += 1
            if self.selected_action > QUIT_GAME:
                self.selected_action = START_GAME

        if key == arcade.key.UP:
            self.selected_action -= 1
            if self.selected_action < START_GAME:
                self.selected_action = QUIT_GAME

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.selected_action == START_GAME:
                game = SpaceGameView()
                game.setup()
                self.window.show_view(game)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0

    def setup(self, score):
        self.score = score

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("GAME OVER", 0, SCREEN_HEIGHT * 0.7,
            font_size = 50, width = SCREEN_WIDTH, align = "center")
        arcade.draw_text(f"Your score was {self.score}\nPress Enter to return to title screen.", 
            0, SCREEN_HEIGHT * 0.4, font_size = 25, width = SCREEN_WIDTH, align = "center")
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            title = TitleView()
            title.setup()
            self.window.show_view(title)

def main():
    window = SpaceGameWindow()
    title = TitleView()
    title.setup()
    window.show_view(title)
    arcade.run()

if __name__ == "__main__":
    main()