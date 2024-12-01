import arcade
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Generic Entity class

class Entity:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.rotation = 0
        self.velocity_rotation = 0

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rotation += self.velocity_rotation

    def draw(self):
        # Draw a red square on screen. This method can be overridden
        # when making new entity types to draw different shapes,
        # sprites, and/or effects
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.RED_BROWN, 0)

    # Debug function that prints entity information to console. Currently unused.
    def print(self, id):
        print("Entity " + str(id) + " at (" + str(self.x) + ", " + str(self.y) + \
            ") with velocity (" + str(self.velocityX) + ", " + str(self.velocityY) + ")")

# Enemy class

# List of enemies currently on screen
enemy_list = []

# Enemy types and their stats
ENEMY_STATS = {
    "basic_straight": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_zigzag": { "health": 1, "velocity_x": (1, 3), "velocity_y": (-3, -1) },
    "basic_wave": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_wait": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_fast": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
    "basic_dodge": { "health": 1, "velocity_x": (0, 0), "velocity_y": (-3, -1) },
}

class Enemy(Entity):
    def __init__(self, type):
        x, y = Enemy.get_coordinates_from_type(type)
        velocity_x, velocity_y = Enemy.get_velocity_from_type(type)
        super().__init__(x, y, velocity_x, velocity_y)
        self.type = type
        self.health = Enemy.get_health_from_type(type)

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.RED_BROWN, 0)

    @staticmethod
    def get_health_from_type(type):
        return ENEMY_STATS[type]["health"]
        
    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*ENEMY_STATS[type]["velocity_x"]), \
            random.uniform(*ENEMY_STATS[type]["velocity_y"])
    
# Obstacle class

# List of obstacles currently on screen
obstacle_list = []

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

class Obstacle(Entity):
    def __init__(self, type):
        x, y = Obstacle.get_coordinates_from_type(type)
        velocity_x, velocity_y, velocity_rotation = Obstacle.get_velocity_from_type(type)
        super().__init__(x, y, velocity_x, velocity_y)
        self.type = type
        self.health = Obstacle.get_health_from_type(type)
        self.velocity_rotation = velocity_rotation

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.ARMY_GREEN, self.rotation)

    @staticmethod
    def get_health_from_type(type):
        return OBSTACLE_STATS[type]["health"]
        
    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*OBSTACLE_STATS[type]["velocity_x"]), \
            random.uniform(*OBSTACLE_STATS[type]["velocity_y"]), \
            random.uniform(*OBSTACLE_STATS[type]["velocity_rotation"])
    
# Collectable class

# List of collectables currently on screen
collectable_list = []

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

class Collectable(Entity):
    def __init__(self, type):
        x, y = Collectable.get_coordinates_from_type(type)
        velocity_x, velocity_y = Collectable.get_velocity_from_type(type)
        super().__init__(x, y, velocity_x, velocity_y)
        self.type = type

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.BLUE_YONDER, 0)

    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*COLLECTABLE_STATS[type]["velocity_x"]), \
            random.uniform(*COLLECTABLE_STATS[type]["velocity_y"])
    
# Bullet class

# List of bullets currently on screen
bullet_list = []

# Bullet types 
BULLET_PLAYER_BASIC = 0
BULLET_PLAYER_HOMING = 1
BULLET_ENEMY_BASIC = 100
BULLET_ENEMY_HOMING = 101

# Bullet default velocity ranges
BULLET_PLAYER_BASIC_VELOCITY_X = (0, 0)
BULLET_PLAYER_BASIC_VELOCITY_Y = (1, 3)
BULLET_ENEMY_BASIC_VELOCITY_X = (0, 0)
BULLET_ENEMY_BASIC_VELOCITY_Y = (-3, -1)

class Bullet(Entity):
    def __init__(self, type):
        x, y = Bullet.get_coordinates_from_type(type)
        velocity_x, velocity_y = Bullet.get_velocity_from_type(type)
        super().__init__(x, y, velocity_x, velocity_y)
        self.type = type

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.DARK_YELLOW, 0)

    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), 0
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*BULLET_PLAYER_BASIC_VELOCITY_X), random.uniform(*BULLET_PLAYER_BASIC_VELOCITY_Y)