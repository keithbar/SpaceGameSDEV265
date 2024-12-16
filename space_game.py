import arcade
import math
import os
import sqlite3
import sys
import random

# Constants

# These values represent the size of the internal canvas. This is
# the number of pixels that will be computed, which will then be
# scaled to the size of the window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
GAME_AREA_LEFT = 620
GAME_AREA_RIGHT = 1300
GAME_AREA_BOTTOM = 110
GAME_AREA_TOP = 1020

# Values concerning the window, including default dimensions.
WINDOW_TITLE = "SDEV 265 Space Game"
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 720

# Obstacle types and their defaul stats
OBSTACLE_STATS = {
    "small":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 1 },
    "small_fast":
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 1 },
    "medium":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-3, 3,), "strength": 2 },
    "medium_fast":
        { "health": 3, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 2 },
    "large":
        { "health": 5, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-1, 1), "strength": 3 },
    "large_fast":
        { "health": 5, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 3 },
    "long":
        { "health": 4, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-3, 3), "strength": 2 },
    "long_fast":
        { "health": 4, "velocity_x": (0, 0), "velocity_y": (-5, -2), \
            "velocity_rotation": (-5, 5), "strength": 2 }
}

# Collectable types and their stats
COLLECTABLE_STATS = {
    "attack_up": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "attack_down": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "defense_up": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "defense_down": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "health_small": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "health_large": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "speed_up": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "speed_down": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "fire_rate_up": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "fire_rate_down": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "bullet_speed_up": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "bullet_speed_down": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "destroy_all_enemies": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
    "invincible": 
        { "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 }
}

PLAYER_SPEED_DEFAULT = 5
PLAYER_SPEED_MAX = 15
PLAYER_SPEED_MIN = 2
PLAYER_COOLDOWN_DEFAULT = 20
PLAYER_COOLDOWN_MAX = 20
PLAYER_COOLDOWN_MIN = 5
MAX_HEALTH_DEFAULT = 5
MAX_HEALTH_MAX = 15
MAX_HEALTH_MIN = 1
INVINCIBLE_TIMER = 900
BULLET_SPEED_DEFAULT = 9
BULLET_SPEED_MAX = 35
BULLET_SPEED_MIN = 9
BULLET_POWER_DEFAULT = 1
BULLET_POWER_MIN = 1
BULLET_POWER_MAX = 10

# Bullet types and their stats
BULLET_STATS = {
    "player_basic": { "velocity_x": (0, 0),
        "velocity_y": (BULLET_SPEED_DEFAULT, BULLET_SPEED_DEFAULT), "friendly": True },
    "enemy_basic": { "velocity_x": (0, 0), "velocity_y": (-8, -8), "friendly": False },
    "enemy_tracker": { "velocity_x": (0, 0), "velocity_y": (0, 0), "friendly": False }
}

# Star properties; sizes must be integers
STAR_SIZE_MIN = 1
STAR_SIZE_MAX = 6
STAR_SPEED_MIN = -1
STAR_SPEED_MAX = -5
NUM_STARS = 100

# Values related to stages
KILL_COUNT_THRESHOLDS = [ 5, 15, 35, 50, 65, 80, 100, 125, 150, 200 ]
ENEMY_SPAWN_TIMERS = [ 180, 180, 150, 120, 120, 120, 90, 90, 60, 30]
OBSTACLE_SPAWN_TIMERS = [ 480, 480, 420, 360, 360, 300, 240, 240, 180, 120 ]
COLLECTABLE_SPAWN_TIMERS = [ 240, 240, 300, 360, 480, 720, 1200, 1800, 2400, 5100]
MAX_STAGE = 10
BETWEEN_STAGE_TIMER = 90
ENEMIES_ON_STAGE = [
    ["basic_straight", "basic_straight", "basic_straight", "basic_wave"],
    ["basic_straight", "basic_straight", "basic_wave", "basic_zigzag"],
    ["basic_straight", "basic_fast", "basic_wave", "basic_zigzag"],
    ["basic_fast", "basic_fast", "basic_wave", "basic_zigzag"],
    ["basic_fast", "basic_wait", "basic_wave", "basic_zigzag"],
    ["basic_fast", "basic_wait", "basic_wave", "basic_wait"],
    ["basic_dodge", "basic_wait", "basic_wave", "basic_wait"],
    ["basic_dodge", "basic_wait", "basic_wave", "basic_wait", "basic_dodge"],
    ["basic_dodge", "basic_wait", "basic_zigzag", "basic_wait", "basic_dodge"],
    ["basic_zigzag", "basic_wave", "basic_wait", "basic_fast", "basic_dodge"]
]
OBSTACLES_ON_STAGE = [
    ["small"],
    ["small"],
    ["small", "medium"],
    ["small", "small_fast", "medium", "medium"],
    ["small_fast", "medium", "medium"],
    ["small_fast", "medium", "large"],
    ["medium_fast", "medium", "large"],
    ["medium_fast", "large", "long"],
    ["medium_fast", "large_fast", "long"],
    ["small", "small_fast", "medium", "medium_fast", "large", "large_fast", "long", "long_fast"]
]
COLLECTABLES_ON_STAGE = [
    ["health_small", "health_small", "health_small", "fire_rate_up"],
    ["health_small", "health_small", "health_small", "defense_up", "fire_rate_up",
        "invincible"],
    ["health_small", "health_small", "health_small", "defense_up", "fire_rate_up",
        "invincible"],
    ["health_small", "health_small", "health_small", "fire_rate_up", "invincible"],
    ["health_small", "speed_up", "speed_down", "fire_rate_up", "fire_rate_down"],
    ["health_small", "speed_up", "speed_down", "fire_rate_up", "fire_rate_down", 
        "bullet_speed_up", "bullet_speed_down"],
    ["health_small", "health_large", "speed_up", "speed_down", "fire_rate_up", 
        "fire_rate_down", "bullet_speed_up", "bullet_speed_down", "defense_up",
        "defense_down"],
    ["health_small", "health_small", "health_small", "health_large", "speed_up",
        "speed_down", "fire_rate_up", "fire_rate_down", "bullet_speed_up",
        "bullet_speed_down", "destroy_all_enemies", "defense_up", "defense_down"],
    ["health_small", "health_small", "health_small", "health_small", "health_small",
        "health_large", "speed_up", "speed_down", "fire_rate_up", "fire_rate_down",
        "bullet_speed_up", "bullet_speed_down", "destroy_all_enemies", "invincible",
        "defense_down"],
    ["health_small", "health_small", "health_small", "health_small", "health_small",
        "health_large", "speed_up", "speed_down", "speed_down", "fire_rate_up",
        "fire_rate_down", "fire_rate_down", "bullet_speed_up", "bullet_speed_down",
        "destroy_all_enemies", "invincible", "defense_up", "defense_down"]
]

# Save data values
# Filename for the savefile
DB_FILENAME = "save.db"
# List of high scores in the following format:
# { { Name, Score }, { Name, Score }, ... }
high_scores = {}
# SQLite database reference
save_db = None

# Flag for displaying debug info
debug_mode = False

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
        
# Enemy types and their stats
ENEMY_STATS = {
    "basic_straight": 
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-4, -2), "score": 100 },
    "basic_zigzag": 
        { "health": 1, "velocity_x": (-3, 3), "velocity_y": (-3, -1), "score": 200 },
    "basic_wave": 
        { "health": 1, "velocity_x": (4, 12), "velocity_y": (-6, -3), "score": 300 },
    "basic_wait": 
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-9, -5), "score": 200 },
    "basic_fast": 
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-20, -13), "score": 200 },
    "basic_dodge": 
        { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1), "score": 100 },
}

SHOOT_COOLDOWN = 40

class Enemy(arcade.Sprite):
    def __init__(self, type):
        flipped_vertically = True
        if type == "basic_straight":
            filename = "./res/img/EnemyShip1.png"
        elif type == "basic_zigzag":
            filename = "./res/img/EnemyShip2.png"
        elif type == "basic_wave":
            filename = "./res/img/EnemyShip3.png"
            flipped_vertically = False
        elif type == "basic_wait":
            filename = "./res/img/EnemyShip4.png"
        elif type == "basic_fast":
            filename = "./res/img/EnemyShip1.png"
        elif type == "basic_dodge":
            filename = "./res/img/EnemyShip5.png"
        else:
            filename = ":resources:images/space_shooter/playerShip3_orange.png"
        scale = 1
        super().__init__(filename, scale, flipped_vertically = flipped_vertically)
        self.center_x = random.uniform(GAME_AREA_LEFT + 20, GAME_AREA_RIGHT - 20)
        self.center_y = SCREEN_HEIGHT + self.height
        self.change_x = random.uniform(*ENEMY_STATS[type]["velocity_x"])
        self.change_y = random.uniform(*ENEMY_STATS[type]["velocity_y"])
        self.type = type
        self.health = ENEMY_STATS[type]["health"]
        self.strength = 1 # Dictates how much damage this enemy does when colliding with player
        self.score = ENEMY_STATS[type]["score"]
        self.shooting = False
        self.shoot_cooldown = SHOOT_COOLDOWN

        if type == "basic_zigzag":
            self.timer = random.uniform(120, 240)
            self.tolerance = 200
        elif type == "basic_wave":
            self.initial_change_x = self.change_x
            self.sine_input = 0.05
            self.sine_input_change = 0.05
        elif type == "basic_wait":
            self.timer_move = random.uniform(40, 120)
            self.timer_wait = random.uniform(40, 80)
            self.zoom = False
        elif type == "basic_dodge":
            self.dodging = False
            self.dodge_direction = 1
            self.tolerance = 75
            self.dodge_time = 5
            self.timer = 0
            self.dodge_speed = 25
            self.dodge_count = random.randint(1, 4)

    def update(self):
        if self.type == "basic_straight":
            self.shoot_cooldown -= 1
            if self.shoot_cooldown < 0:
                shoot_random_value = random.uniform(0, 100)
                if shoot_random_value < 0.2:
                    self.shooting = True
                    self.shoot_cooldown = SHOOT_COOLDOWN

        elif self.type == "basic_zigzag":
            self.timer -= 1
            self.shoot_cooldown -= 1
            if self.timer < 0:
                self.change_x = -self.change_x
                self.timer = random.uniform(120, 240)

        elif self.type == "basic_wave":
            self.change_x = math.sin(self.sine_input) * self.initial_change_x
            self.sine_input += self.sine_input_change

        elif self.type == "basic_wait":
            self.shoot_cooldown -= 1
            if self.change_y < 0 and not self.zoom:
                self.timer_move -= 1
                if self.timer_move < 0:
                    self.change_y = 0
            elif self.change_y == 0:
                self.timer_wait -= 1
                if self.timer_wait < 0:
                    self.zoom = True
                    self.change_y = random.uniform(-20, -12)

        elif self.type == "basic_dodge":
            if self.dodging:
                self.timer -= 1
                if self.timer > 0:
                    if self.dodge_direction > 0:
                        self.change_x = self.dodge_speed
                    else:
                        self.change_x = -self.dodge_speed
                else:
                    self.dodging = False
                    self.timer = self.dodge_time
                    self.change_x = 0
        return super().update()

# Class for the main game loop, extends Arcade's View class
class SpaceGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_list = None
        self.bullet_list = None
        self.obstacle_list = None
        self.collectable_list = None
        self.explosion_list = None
        self.player_shield = None

        # Stuff for hud
        self.hud_frame = None
        self.bg_moon = None

        self.enemy_spawn_timer = ENEMY_SPAWN_TIMERS[0]
        self.obstacle_spawn_timer = OBSTACLE_SPAWN_TIMERS[0]
        self.collectable_spawn_timer = COLLECTABLE_SPAWN_TIMERS[0]
        
        #This is for the enemies when implamented 
        self.enemy_list = None
        self.enemy_direction = 1
        
        #initializes our score and sets us up to implament the game over when you lose and add new waves in the future
        self.score = 0
        self.kills = 0
        self.game_over = False
        self.enemies_spawned = 0
        self.stage = 1
        self.paused = False
        self.between_stage_timer = BETWEEN_STAGE_TIMER

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.collectable_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.star_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.player_shield = arcade.SpriteCircle(100, arcade.color.BABY_BLUE, True)
        self.player_shield.alpha = 150
        self.hud_frame = arcade.Sprite("./res/img/hud_frame.png", 
            center_x = SCREEN_WIDTH // 2, center_y = SCREEN_HEIGHT // 2)
        self.bg_moon = arcade.Sprite("./res/img/bg_moon.png", 
            center_x = SCREEN_WIDTH // 2, center_y = -100)
        self.score = 0
        self.kills = 0
        self.enemies_spawned = 0
        self.game_over = False  
        self.stage = 1
        self.paused = False
        self.between_stage_timer = 0
         
        # This is our player I tried to find different sprites but this is what I have for now 
        self.player = arcade.Sprite("./res/img/Player Ship.png")
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 200
        self.player.moving_left = False
        self.player.moving_right = False
        self.player.moving_up = False
        self.player.moving_down = False
        self.player.health_max = MAX_HEALTH_DEFAULT
        self.player.health = MAX_HEALTH_DEFAULT
        self.player.invincible_timer = 0
        self.player.current_speed = PLAYER_SPEED_DEFAULT
        self.player.current_bullet_speed = BULLET_SPEED_DEFAULT
        self.player.current_bullet_power = BULLET_POWER_DEFAULT
        self.player.shoot_cooldown_initial = PLAYER_COOLDOWN_DEFAULT
        self.player.shoot_cooldown = 0
        self.player_list.append(self.player)

        # Spawn the initial stars
        for _ in range(NUM_STARS):
            self.spawn_star(True)
        
    # Drawing method that is called on every frame
    def on_draw(self):
        arcade.start_render()

        self.star_list.draw()
        self.bg_moon.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.obstacle_list.draw()
        self.collectable_list.draw()
        self.explosion_list.draw()

        if self.player.invincible_timer > 0:
            self.player_shield.center_x = self.player.center_x
            self.player_shield.center_y = self.player.center_y
            self.player_shield.draw()

        # Draw hud on top of everything else
        self.hud_frame.draw()
        arcade.draw_text(f"Score: {self.score}", 20, 180, arcade.color.WHITE, 30,
                         font_name = "Kenney Mini Square")
        arcade.draw_text(f"Stage: {self.stage}", 20, 80, arcade.color.WHITE, 30,
                         font_name = "Kenney Mini Square")
        
        # Debug info
        global debug_mode
        if debug_mode:
            arcade.draw_text(f"Health: {self.player.health}/{self.player.health_max}", 10, 20)
            arcade.draw_text(f"Shoot cooldown: {self.player.shoot_cooldown}", 10, 50)
            arcade.draw_text(f"Bullet power: {self.player.current_bullet_power}", 10, 80)
            arcade.draw_text(f"Bullet speed: {self.player.current_bullet_speed}", 10, 110)
            arcade.draw_text(f"Speed: {self.player.current_speed}", 10, 140)
            arcade.draw_text(f"Invincible timer: {self.player.invincible_timer}", 10, 170)
            arcade.draw_text(f"Between stage timer: {self.between_stage_timer}", 10, 200)
            arcade.draw_text(f"enemy spawn timer: {self.enemy_spawn_timer}", 10, 230)
            arcade.draw_text(f"enemy spawn count: {self.enemies_spawned}", 10, 260)
            for enemy in self.enemy_list:
                arcade.draw_text(f"Health: {enemy.health}", enemy.center_x + 20, enemy.center_y)
            for obstacle in self.obstacle_list:
                arcade.draw_text(f"Health: {obstacle.health}", obstacle.center_x + 20, obstacle.center_y)
            for collectable in self.collectable_list:
                arcade.draw_text(collectable.type, collectable.center_x + 10, collectable.center_y)

        # Draw the pause overlay
        if self.paused:
            # These draw functions accept colors in RGB or RGBA format. The built in colors,
            # like arcade.color.BLACK, are RGB format. Adding (200,) adds an alpha value to
            # make it RGBA, allowing for transparency.
            arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.BLACK + (200,))
            arcade.draw_text("PAUSED", 0, SCREEN_HEIGHT / 2, font_size = 30,
                width = SCREEN_WIDTH, align = "center", font_name = "Kenney Pixel Square")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.moving_left = True

        elif key == arcade.key.RIGHT:
            self.player.moving_right = True

        elif key == arcade.key.UP:
            self.player.moving_up = True

        elif key == arcade.key.DOWN:
            self.player.moving_down = True
        
        #This is the projectile I found that looked the best so far however we can change for whatever everyone likes 
        elif key == arcade.key.SPACE and not self.paused and self.player.shoot_cooldown < 0:
            self.spawn_bullet("player_basic", self.player.center_x, self.player.center_y + 20)
            self.player.shoot_cooldown = self.player.shoot_cooldown_initial

        elif key == arcade.key.ENTER:
            self.paused = not self.paused

    def update(self, delta_time):
        if self.player.health <= 0:
            game_over = GameOverView()
            game_over.setup(self.score)
            self.window.show_view(game_over)
            return
        
        if self.paused:
            return

        # Update the player's movement and timers
        if self.player.moving_left and not self.player.moving_right:
            self.player.change_x = -self.player.current_speed
        elif self.player.moving_right and not self.player.moving_left:
            self.player.change_x = self.player.current_speed
        else:
            self.player.change_x = 0
        
        if self.player.moving_up and not self.player.moving_down:
            self.player.change_y = self.player.current_speed
        elif self.player.moving_down and not self.player.moving_up:
            self.player.change_y = -self.player.current_speed
        else:
            self.player.change_y = 0
        self.player.shoot_cooldown -= 1
        self.player.invincible_timer -= 1

        self.between_stage_timer -= 1

        self.star_list.update()
        self.player_list.update()
        self.bullet_list.update()
        self.enemy_list.update()
        self.obstacle_list.update()
        self.collectable_list.update()
        self.explosion_list.update_animation()

        for explosion in self.explosion_list:
            explosion.timer -= 1
            if explosion.timer < 0:
                explosion.remove_from_sprite_lists()

        # This is what keeps our ship confined to our screen
        if self.player.left < GAME_AREA_LEFT:
            self.player.left = GAME_AREA_LEFT

        elif self.player.right > GAME_AREA_RIGHT:
            self.player.right = GAME_AREA_RIGHT

        if self.player.bottom < GAME_AREA_BOTTOM:
            self.player.bottom = GAME_AREA_BOTTOM

        elif self.player.top > GAME_AREA_TOP:
            self.player.top = GAME_AREA_TOP

        # Remove entities that have moved off screen
        self.cull_off_screen()

        # Check for collision between entities
        self.check_collision()

        # Spawn all entities
        self.spawn_entities()

        self.enemy_shooting()
    
    #Updates button press on release so that we dont continue moving
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.moving_left = False
        elif key == arcade.key.RIGHT:
            self.player.moving_right = False
        elif key == arcade.key.UP:
            self.player.moving_up = False
        elif key == arcade.key.DOWN:
            self.player.moving_down = False

    def cull_off_screen(self):
        # Removes the bullets that are off screen 
        for bullet in self.bullet_list:
            if bullet.bottom > SCREEN_HEIGHT or bullet.top < 0:
                bullet.remove_from_sprite_lists()

        # Removes enemies that are off screen
        for enemy in self.enemy_list:
            if enemy.top < 0:
                type = enemy.type
                enemy.remove_from_sprite_lists()
                self.spawn_enemy(type)

        # Removes obstacles that are off screen
        for obstacle in self.obstacle_list:
            if obstacle.top < 0:
                obstacle.remove_from_sprite_lists()

        # Removes collectables that are off screen
        for collectable in self.collectable_list:
            if collectable.top < 0:
                collectable.remove_from_sprite_lists()

        # Removes stars that are off screen and spawns new ones
        for star in self.star_list:
            if star.center_y < -5:
                star.remove_from_sprite_lists()
                self.spawn_star()

    def check_collision(self):
        for player in self.player_list:

            # If player is not invincible
            if player.invincible_timer < 0:
                # Check for player-enemy collisions
                player_enemy_collision = arcade.check_for_collision_with_list(
                    player, self.enemy_list
                )
                # Decrement player health and destroy enemy
                for enemy in player_enemy_collision:
                    player.health -= enemy.strength
                    self.spawn_explosion(enemy.center_x, enemy.center_y)
                    enemy.remove_from_sprite_lists()

                # Check for player-bullet collisions
                player_bullet_collision = arcade.check_for_collision_with_list(
                    player, self.bullet_list
                )
                for bullet in player_bullet_collision:
                    if bullet.friendly == False:
                        player.health -= bullet.strength
                        self.spawn_explosion(bullet.center_x, bullet.center_y, "small")
                        bullet.remove_from_sprite_lists()

                # Check for player-obstacle collisions
                player_obstacle_collision = arcade.check_for_collision_with_list(
                    player, self.obstacle_list
                )
                for obstacle in player_obstacle_collision:
                    player.health -= obstacle.strength
                    self.spawn_explosion(obstacle.center_x, obstacle.center_y)
                    obstacle.remove_from_sprite_lists()

            # Check for player-collectable collisions
            player_collectable_collision = arcade.check_for_collision_with_list(
                player, self.collectable_list
            )
            for collectable in player_collectable_collision:
                self.collect_collectable(player, collectable.type)
                self.score += collectable.score
                collectable.remove_from_sprite_lists()

        # Check for enemy-bullet collisions
        for bullet in self.bullet_list:
            if bullet.friendly == True:
                enemy_bullet_collision = arcade.check_for_collision_with_list(
                    bullet, self.enemy_list
                )
                for enemy in enemy_bullet_collision:
                    enemy.health -= bullet.strength
                    if enemy.health <= 0:
                        self.score += enemy.score
                        self.kills += 1
                        self.set_stage()
                        enemy.remove_from_sprite_lists()
                        self.spawn_explosion(enemy.center_x, enemy.center_y)
                    else:
                        self.spawn_explosion(bullet.center_x, bullet.center_y, "small")
                    bullet.remove_from_sprite_lists()
                    
                    # Break so one bullet doesn't affect multiple enemies
                    break

        # Check for obstacle-bullet collisions
        for bullet in self.bullet_list:
            if bullet.friendly == True:
                obstacle_bullet_collision = arcade.check_for_collision_with_list(
                    bullet, self.obstacle_list
                )
                for obstacle in obstacle_bullet_collision:
                    obstacle.health -= bullet.strength
                    if obstacle.health <= 0:
                        self.spawn_explosion(obstacle.center_x, obstacle.center_y)
                        obstacle.remove_from_sprite_lists()
                    else:
                        self.spawn_explosion(bullet.center_x, bullet.center_y, "small")
                    bullet.remove_from_sprite_lists()
                    break

        # Do a special check for dodging enemies
        for enemy in self.enemy_list:
            if enemy.type == "basic_dodge" and enemy.dodge_count > 0 and not enemy.dodging:
                for bullet in self.bullet_list:
                    if bullet.friendly == True:
                        distance = arcade.get_distance_between_sprites(enemy, bullet)
                        if distance < enemy.tolerance:
                            enemy.dodging = True
                            enemy.dodge_direction = enemy.center_x - bullet.center_x
                            enemy.dodge_count -= 1
                            enemy.timer = enemy.dodge_time

    def set_stage(self):
        if self.stage < MAX_STAGE and \
            self.kills >= KILL_COUNT_THRESHOLDS[self.stage - 1]:
                self.stage += 1
                self.between_stage_timer = BETWEEN_STAGE_TIMER
    
    def spawn_explosion(self, center_x, center_y, type = "large"):
        if type == "large":
            explosion = arcade.load_animated_gif("./res/img/explosion1.gif")
            explosion.scale = 1
            explosion.timer = 60
        else:
            explosion = arcade.Sprite("./res/img/spark.png")
            explosion.scale = 0.5
            explosion.timer = 3
        explosion.center_x = center_x
        explosion.center_y = center_y
        self.explosion_list.append(explosion)

    # Spawns a new enemy of the given type (see ENEMY_STATS above)
    def spawn_enemy(self, type):
        enemy = Enemy(type)
        self.enemy_list.append(enemy)

    # Spawns a new obstacle of the given type (see OBSTACLE_STATS above)
    def spawn_obstacle(self, type):
        if type == "small" or type == "small_fast":
            image = "./res/img/Space Meatball.png"
            scale = 0.6
        elif type == "medium" or type == "medium_fast":
            image = "./res/img/Space Meatball.png"
            scale = 1
        elif type == "large" or type == "large_fast":
            image = "./res/img/Space Meatball.png"
            scale = 2
        else:
            image = "./res/img/space_debris.png"
            scale = 0.7
        obstacle = arcade.Sprite(image, scale)
        obstacle.center_x = random.uniform(GAME_AREA_LEFT, GAME_AREA_RIGHT)
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
        scale = 0.2
        if type == "health_small":
            filename = "./res/img/Gold.png"
        elif type == "health_large":
            filename = "./res/img/Gold.png"
            scale = 2
        elif type == "attack_up":
            filename = "./res/img/Buff-Debbuf 13.png"
        elif type == "attack_down":
            filename = "./res/img/Buff-Debbuf 12.png"
        elif type == "defense_up":
            filename = "./res/img/Buff-Debbuf 3.png"
        elif type == "defense_down":
            filename = "./res/img/Buff-Debbuf 4.png"
        elif type == "speed_up":
            filename = "./res/img/Buff-Debbuf 10.png"
        elif type == "speed_down":
            filename = "./res/img/Buff-Debbuf 11.png"
        elif type == "fire_rate_up":
            filename = "./res/img/Buff-Debbuf 15.png"
        elif type == "fire_rate_down":
            filename = "./res/img/Buff-Debbuf 14.png"
        elif type == "bullet_speed_up":
            filename = "./res/img/Buff-Debbuf 8.png"
        elif type == "bullet_speed_down":
            filename = "./res/img/Buff-Debbuf 9.png"
        elif type == "destroy_all_enemies":
            filename = "./res/img/Buff-Debbuf 1.png"
        elif type == "invincible":
            filename = "./res/img/Buff-Debbuf 7.png"
        else:
            filename = "./res/img/Buff-Debbuf 13.png"
        
        collectable = arcade.Sprite(filename, scale)
        collectable.center_x = random.uniform(GAME_AREA_LEFT, GAME_AREA_RIGHT)
        collectable.center_y = SCREEN_HEIGHT + collectable.height
        collectable.change_x = random.uniform(*COLLECTABLE_STATS[type]["velocity_x"])
        collectable.change_y = random.uniform(*COLLECTABLE_STATS[type]["velocity_y"])
        collectable.type = type
        collectable.score = COLLECTABLE_STATS[type]["score"]
        self.collectable_list.append(collectable)

    # Spawns a new bullet of the given type (see BULLET_STATS above)
    def spawn_bullet(self, type, x, y):
        friendly = BULLET_STATS[type]["friendly"]
        bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", 0.8)
        bullet.center_x = x
        bullet.center_y = y
        bullet.change_x = random.uniform(*BULLET_STATS[type]["velocity_x"])
        bullet.change_y = random.uniform(*BULLET_STATS[type]["velocity_y"])
        bullet.friendly = friendly
        bullet.strength = 1

        if type == "enemy_tracker":
            angle = arcade.get_angle_degrees(
                bullet.center_x, bullet.center_y,
                self.player.center_x, self.player.center_y
            )
            bullet.change_x = 15 * math.sin(math.radians(angle))
            bullet.change_y = 15 * math.cos(math.radians(angle))
            bullet.angle = -angle
        
        elif type == "player_basic":
            bullet.change_y = self.player.current_bullet_speed
            bullet.strength = self.player.current_bullet_power

        self.bullet_list.append(bullet)

    # Contains all logic for spawning entities based on stage, time passed, etc.
    def spawn_entities(self):
        if self.between_stage_timer < 0:

            # Spawn enemies
            self.enemy_spawn_timer -= 1
            if self.enemy_spawn_timer < 0 and \
                self.enemies_spawned < KILL_COUNT_THRESHOLDS[self.stage - 1]:
                    enemy_type = random.choice(list(ENEMIES_ON_STAGE[self.stage - 1]))
                    self.spawn_enemy(enemy_type)
                    new_timer = ENEMY_SPAWN_TIMERS[self.stage - 1]
                    self.enemy_spawn_timer = random.uniform(new_timer * 0.9, new_timer * 1.1)
                    self.enemies_spawned += 1

            # Spawn obstacles
            self.obstacle_spawn_timer -= 1
            if self.obstacle_spawn_timer < 0:
                obstacle_type = random.choice(list(OBSTACLES_ON_STAGE[self.stage - 1]))
                self.spawn_obstacle(obstacle_type)
                new_timer = OBSTACLE_SPAWN_TIMERS[self.stage - 1]
                self.obstacle_spawn_timer = random.uniform(new_timer * 0.9, new_timer * 1.1)

            # Spawn collectables
            self.collectable_spawn_timer -= 1
            if self.collectable_spawn_timer < 0:
                collectable_type = random.choice(list(COLLECTABLES_ON_STAGE[self.stage - 1]))
                self.spawn_collectable(collectable_type)
                new_timer = COLLECTABLE_SPAWN_TIMERS[self.stage - 1]
                self.collectable_spawn_timer = random.uniform(new_timer * 0.9, new_timer * 1.1)
                

    # Spawns a new background star. If part of the initial batch of stars
    # spawned at beginning of game, it will be place on the screen randomly.
    # Otherwise, it will be placed at the top of the screen.
    def spawn_star(self, initial = False):
        star_size = random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)

        color_random = random.uniform(0, 100)
        if color_random < 70:
            star_color = arcade.color.WHITE
        elif color_random < 80:
            star_color = arcade.color.WHITE_SMOKE
        elif color_random < 90:
            star_color = arcade.color.LIGHT_BLUE
        elif color_random < 95:
            star_color = arcade.color.PASTEL_ORANGE
        else:
            star_color = arcade.color.RED_ORANGE

        star = arcade.SpriteCircle(star_size, star_color, True)

        if initial:
            star.center_y = random.uniform(0, SCREEN_HEIGHT)
        else:
            star.center_y = SCREEN_HEIGHT + 5

        star.center_x = random.uniform(GAME_AREA_LEFT, GAME_AREA_RIGHT)
        star.change_y = random.uniform(STAR_SPEED_MAX, STAR_SPEED_MIN)
        self.star_list.append(star)

    # Applies collectable effects to given player
    def collect_collectable(self, player, type):
        if type == "attack_up":
            player.current_bullet_power += 1
            if player.current_bullet_power > BULLET_POWER_MAX:
                player.current_bullet_power = BULLET_POWER_MAX
        elif type == "attack_down":
            player.current_bullet_power -= 1
            if player.current_bullet_power < BULLET_POWER_MIN:
                player.current_bullet_power = BULLET_POWER_MIN
        elif type == "defense_up":
            player.health_max += 1
            if player.health_max > MAX_HEALTH_MAX:
                player.health_max = MAX_HEALTH_MAX
        elif type == "defense_down":
            player.health_max -= 1
            if player.health_max < MAX_HEALTH_MIN:
                player.health_max = MAX_HEALTH_MIN
            if player.health > player.health_max:
                player.health = player.health_max
        elif type == "health_small":
            player.health += 1
            if player.health > player.health_max:
                player.health = player.health_max
        elif type == "health_large":
            player.health = player.health_max
        elif type == "speed_up":
            player.current_speed += 1
            if player.current_speed > PLAYER_SPEED_MAX:
                player.current_speed = PLAYER_SPEED_MAX
        elif type == "speed_down":
            player.current_speed -= 1
            if player.current_speed < PLAYER_SPEED_MIN:
                player.current_speed = PLAYER_SPEED_MIN
        elif type == "fire_rate_up":
            player.shoot_cooldown_initial -= 4
            if player.shoot_cooldown_initial < PLAYER_COOLDOWN_MIN:
                player.shoot_cooldown_initial = PLAYER_COOLDOWN_MIN
        elif type == "fire_rate_down":
            player.shoot_cooldown_initial += 4
            if player.shoot_cooldown_initial > PLAYER_COOLDOWN_MAX:
                player.shoot_cooldown_initial = PLAYER_COOLDOWN_MAX
        elif type == "bullet_speed_up":
            player.current_bullet_speed += 3
            if player.current_bullet_speed > BULLET_SPEED_MAX:
                player.current_bullet_speed = BULLET_POWER_MAX
        elif type == "bullet_speed_down":
            player.current_bullet_speed -= 3
            if player.current_bullet_speed < BULLET_SPEED_MIN:
                player.current_bullet_speed = BULLET_SPEED_MIN
        elif type == "destroy_all_enemies":
            for enemy in self.enemy_list:
                self.score += enemy.score
                self.kills += 1
                self.spawn_explosion(enemy.center_x, enemy.center_y)
            self.enemy_list.clear()
            for obstacle in self.obstacle_list:
                self.spawn_explosion(obstacle.center_x, obstacle.center_y)
            self.obstacle_list.clear()
            self.set_stage()
        elif type == "invincible":
            self.player.invincible_timer = INVINCIBLE_TIMER

    def enemy_shooting(self):
        for enemy in self.enemy_list:
            # Do a special check for zigzaggers who only shoot when the player is below them
            if enemy.type == "basic_zigzag" and enemy.shoot_cooldown < 0:
                if abs(enemy.center_x - self.player.center_x) < enemy.tolerance:
                    random_value = random.uniform(0, 100)
                    if random_value < 1:
                        enemy.shooting = True
                        enemy.shoot_cooldown = SHOOT_COOLDOWN

            # Do a special check for waiters who always shoot when waiting
            elif enemy.type == "basic_wait" and enemy.change_y == 0 \
                    and enemy.shoot_cooldown < 0:
                self.spawn_bullet("enemy_tracker", enemy.center_x, enemy.center_y)
                enemy.shoot_cooldown = SHOOT_COOLDOWN // 4

            if enemy.shooting and not enemy.type == "basic_wait":
                enemy.shooting = False
                self.spawn_bullet("enemy_basic", enemy.center_x, enemy.center_y)

START_GAME = 0
HIGH_SCORE = 1
SETTINGS = 2
QUIT_GAME = 3

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_action = START_GAME
        self.bg_moon = None

    # setup is currently redundant, left it here in case we want to
    # do more with it in the future
    def setup(self):
        self.selected_action = START_GAME
        self.bg_moon = self.bg_moon = arcade.Sprite("./res/img/bg_moon.png", 
            center_x = SCREEN_WIDTH // 2, center_y = 0)

    def on_draw(self):
        arcade.start_render()

        self.bg_moon.draw()

        arcade.draw_text("SDEV 265\nSPACE GAME", 0, SCREEN_HEIGHT * 0.7,
            font_size = 50, width = SCREEN_WIDTH, align = "center",
            font_name = "Kenney Blocks")
        
        # Values to make changing text layout easier
        option_font_size = 25
        option_line_height = 35
        option_y_start = SCREEN_HEIGHT * 0.4
        options_font = "Kenney Mini Square"

        text_start_game = arcade.Text(" Start Game ", 0, option_y_start, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center",
            font_name = options_font)
        text_start_game.draw()

        text_high_score = arcade.Text(" High Scores ", 0, option_y_start - option_line_height, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center",
            font_name = options_font)
        text_high_score.draw()

        text_settings = arcade.Text(" Settings ", 0, option_y_start - option_line_height * 2, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center",
            font_name = options_font)
        text_settings.draw()

        text_quit = arcade.Text(" Quit ", 0, option_y_start - option_line_height * 3, 
            font_size = option_font_size, width = SCREEN_WIDTH, align = "center",
            font_name = options_font)
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
            elif self.selected_action == HIGH_SCORE:
                high_score = HighScoreView()
                high_score.setup()
                self.window.show_view(high_score)
            elif self.selected_action == SETTINGS:
                settings = SettingsView()
                self.window.show_view(settings)
            elif self.selected_action == QUIT_GAME:
                arcade.exit()

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.new_high_score = False
        self.replace_score_id = 0
        self.initials = []
        self.initials_colors = []
        self.selected_initial = 0

    def setup(self, score):
        self.score = score
        global save_db
        # Grab the lowest score in the leaderboard for comparison
        lowest_score = save_db.execute("SELECT *, MIN(SCORE) FROM SCORES").fetchall()
        if score <= lowest_score[0][2]:
            # Score is too low for leaderboards, set flag accordingly
            self.new_high_score = False
        else:
            # The player has set a high score
            self.new_high_score = True
            self.replace_score_id = lowest_score[0][0]
            # Initialize an array of characters used for the name entry screen
            self.initials = ['A', 'A', 'A']
            # Set the color of the selected initial as red
            self.initials_colors = [arcade.color.RED, arcade.color.WHITE, arcade.color.WHITE]

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("GAME OVER", 0, SCREEN_HEIGHT * 0.7,
            font_size = 50, width = SCREEN_WIDTH, align = "center", font_name = "Kenney Rocket")
        if self.new_high_score:
            arcade.draw_text(f"Your score was {self.score}\nNew high score set!\nEnter your initials.", \
                0, SCREEN_HEIGHT * 0.4, font_size = 25, width = SCREEN_WIDTH, align = "center",
                font_name = "Kenney Rocket")
            
            arcade.draw_text(self.initials[0], 0, SCREEN_HEIGHT * .5, \
                color = self.initials_colors[0], font_size = 80, width = SCREEN_WIDTH * .4, align = "right",
                font_name = "Kenney Blocks")
            arcade.draw_text(self.initials[1], 0, SCREEN_HEIGHT * .5, \
                color = self.initials_colors[1], font_size = 80, width = SCREEN_WIDTH, align = "center",
                font_name = "Kenney Blocks")
            arcade.draw_text(self.initials[2], SCREEN_WIDTH * .6, SCREEN_HEIGHT * .5, \
                color = self.initials_colors[2], font_size = 80, width = SCREEN_WIDTH * .4, align = "left",
                font_name = "Kenney Blocks")
        else:
            arcade.draw_text(f"Your score was {self.score}\nPress Enter to return to title screen.", 
                0, SCREEN_HEIGHT * 0.4, font_size = 25, width = SCREEN_WIDTH, align = "center",
                font_name = "Kenney Rocket")
        
    def on_key_press(self, key, moddifiers):
        # Left and Right will change which initial is being modified,
        # setting the colors accordingly
        if self.new_high_score:
            if key == arcade.key.LEFT:
                self.initials_colors[self.selected_initial] = arcade.color.WHITE
                self.selected_initial -= 1
                if self.selected_initial < 0:
                    self.selected_initial = 2
                self.initials_colors[self.selected_initial] = arcade.color.RED
            elif key == arcade.key.RIGHT:
                self.initials_colors[self.selected_initial] = arcade.color.WHITE
                self.selected_initial += 1
                if self.selected_initial > 2:
                    self.selected_initial = 0
                self.initials_colors[self.selected_initial] = arcade.color.RED
            
            # Up and Down will the change the character displayed
            elif key == arcade.key.UP:
                new_char = chr(ord(self.initials[self.selected_initial]) + 1)
                if ord(new_char) > ord('Z'):
                    new_char = 'A'
                self.initials[self.selected_initial] = new_char
            elif key == arcade.key.DOWN:
                new_char = chr(ord(self.initials[self.selected_initial]) - 1)
                if ord(new_char) < ord('A'):
                    new_char = 'Z'
                self.initials[self.selected_initial] = new_char

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.new_high_score:
                # Combine the initials into a single string
                name = self.initials[0] + self.initials[1] + self.initials[2]
                # Save the score to the database
                save_score(name, self.score, self.replace_score_id)
            title = TitleView()
            title.setup()
            self.window.show_view(title)

class HighScoreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_moon = None

    def setup(self):
        # Ensure the most up-to-date scores are loaded
        load_game()
        self.bg_moon = arcade.Sprite(filename = "./res/img/bg_moon.png", scale = 2, center_x = -150, center_y = SCREEN_HEIGHT // 2)
        self.bg_moon.color = arcade.color.RED
        self.bg_moon.alpha = 100

    def on_draw(self):
        arcade.start_render()
        self.bg_moon.draw()
        arcade.draw_text("HIGH SCORES", 0, SCREEN_HEIGHT * .8, font_size = 25, \
                         width = SCREEN_WIDTH, align = "center",
                         font_name = "Kenney Rocket")
        score_rank = 1
        print_y = SCREEN_HEIGHT * .7
        line_height = 50
        global high_scores
        for score in high_scores:
            arcade.draw_text(
                f"{score_rank}. {high_scores[score_rank - 1][1]}: {high_scores[score_rank - 1][2]}", \
                0, print_y, font_size = 30, width = SCREEN_WIDTH, align = "center",
                font_name = "Kenney High Square")
            score_rank += 1
            print_y -= line_height

        arcade.draw_text("Press ENTER to return", 0, SCREEN_HEIGHT * .15, \
                         font_size = 12, width = SCREEN_WIDTH, align = "center",
                         font_name = "Kenney Pixel Square")
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            title = TitleView()
            title.setup()
            self.window.show_view(title)

DELETE_SCORES = 0
RETURN_TO_TITLE = 1
CONFIRM_NO = 2
CONFIRM_YES = 3

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.delete_confirmation = False
        self.selected_action = DELETE_SCORES

    def on_draw(self):
        arcade.start_render()
        print_y = SCREEN_HEIGHT * .7
        line_height = 45
        font_name = "Kenney Pixel Square"
        text_delete_scores = arcade.Text("  Reset high scores  ", 0, print_y, \
            font_size = 25, width = SCREEN_WIDTH, align = "center", font_name = font_name)
        text_return_to_tile = arcade.Text("  Return to title screen  ", 0, print_y - line_height * 5, \
            font_size = 25, width = SCREEN_WIDTH, align = "center", font_name = font_name)
        text_confirmation = arcade.Text("Are you sure?", 0, print_y - line_height, \
            font_size = 25, width = SCREEN_WIDTH, align = "center", font_name = font_name)
        text_confirmation_no = arcade.Text("  No  ", 0, print_y - line_height * 2, \
            font_size = 25, width = SCREEN_WIDTH, align = "center", font_name = font_name)
        text_confirmation_yes = arcade.Text("  Yes  ", 0, print_y - line_height * 3, \
            font_size = 25, width = SCREEN_WIDTH, align = "center", font_name = font_name)
        
        text_delete_scores.draw()
        text_return_to_tile.draw()

        if self.delete_confirmation:
            text_confirmation.draw()
            text_confirmation_no.draw()
            text_confirmation_yes.draw()

        if self.selected_action == DELETE_SCORES:
            selected_text = text_delete_scores
        elif self.selected_action == RETURN_TO_TITLE:
            selected_text = text_return_to_tile
        elif self.selected_action == CONFIRM_NO:
            selected_text = text_confirmation_no
        else:
            selected_text = text_confirmation_yes

        arrow_size = 25
        text_width = selected_text.content_width
        arrow_left_x = SCREEN_WIDTH / 2 - text_width / 2 - arrow_size
        arrow_y = selected_text.y
        arcade.draw_triangle_filled(
            arrow_left_x, arrow_y, 
            arrow_left_x, arrow_y + arrow_size,
            arrow_left_x + arrow_size, arrow_y + arrow_size / 2,
            arcade.color.WHITE
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.selected_action += 1
            if not self.delete_confirmation and self.selected_action > 1:
                self.selected_action = 0
            elif self.delete_confirmation and self.selected_action > 3:
                self.selected_action = 2
        elif key == arcade.key.UP:
            self.selected_action -= 1
            if not self.delete_confirmation and self.selected_action < 0:
                self.selected_action = 1
            elif self.delete_confirmation and self.selected_action < 2:
                self.selected_action = 3

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.selected_action == DELETE_SCORES:
                self.delete_confirmation = True
                self.selected_action = CONFIRM_NO
            elif self.selected_action == RETURN_TO_TITLE:
                title = TitleView()
                title.setup()
                self.window.show_view(title)
            elif self.selected_action == CONFIRM_NO:
                self.delete_confirmation = False
                self.selected_action = DELETE_SCORES
            elif self.selected_action == CONFIRM_YES:
                init_save(True)
                self.delete_confirmation = False
                self.selected_action = DELETE_SCORES
        
# Reads all the scores from the database into an easily accessible list
def load_game():
    global high_scores
    global save_db
    high_scores = save_db.execute("SELECT * FROM SCORES ORDER BY SCORE DESC").fetchall()

# Updates the leaderboard with the given name and score, replacing the existing
# score represented by replace_id in the database
def save_score(name, score, replace_id):
    global save_db
    save_db.execute(f'''UPDATE SCORES SET NAME = "{name}", SCORE = {score}
                    WHERE ID = {replace_id}''')
    save_db.commit()

# Ensures that a valid save file exists. Used in init_save to overwrite potentially
# corrupted save files with brand new ones.
def validate_save():
    global save_db
    global high_scores

    # Save file does not exist
    if not os.path.exists(DB_FILENAME):
        return False
    
    # Can't connect to database
    try:
        save_db = sqlite3.connect(DB_FILENAME)
    except:
        return False
    
    # Score table not present in save file
    try:
        high_scores = save_db.execute('''SELECT * FROM SCORES''').fetchall()
    except:
        return False
    
    # Incorrect number of scores present
    if len(high_scores) != 10:
        return False
    
    # Incorrect score format
    try:
        schema = save_db.execute('''PRAGMA table_info('SCORES')''').fetchall()
        if len(schema) != 3 or \
            schema[0][1] != "ID" or schema[0][2] != "INTEGER" or schema[0][5] != 1 or \
            schema[1][1] != "NAME" or schema[1][2] != "TEXT" or schema[1][5] != 0 or \
            schema[2][1] != "SCORE" or schema[2][2] != "INT" or schema[2][5] != 0:
                return False
    except:
        return False
    
    # All checks pass, save is (probably) valid
    return True

# Initializes a new save file if one doesn't already exist,
# populating the leaderboard with default values
def init_save(reset = False):
    global save_db
    save_db = sqlite3.connect(DB_FILENAME)
    if reset or not validate_save():
        if os.path.exists(DB_FILENAME):
            save_db.close()
            save_db = None
            os.remove(DB_FILENAME)
            save_db = sqlite3.connect(DB_FILENAME)
        save_db.execute('''CREATE TABLE SCORES (
                            ID INTEGER PRIMARY KEY,
                            NAME TEXT NOT NULL,
                            SCORE INT NOT NULL
                        )''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test01", 1)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test02", 2)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test03", 3)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test04", 4)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test05", 5)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test06", 6)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test07", 7)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test08", 8)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test09", 9)''')
        save_db.execute('''INSERT INTO SCORES(NAME, SCORE)
                            VALUES("test10", 10)''')
        save_db.commit()

def main():
    global debug_mode
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug_mode = True
    init_save()
    load_game()
    window = SpaceGameWindow()
    title = TitleView()
    title.setup()
    window.show_view(title)
    arcade.run()

if __name__ == "__main__":
    main()