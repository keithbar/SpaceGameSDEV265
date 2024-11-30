import arcade
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Generic Entity class

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

# Enemy class

# List of enemies currently on screen
enemy_list = []

# Enemy types
ENEMY_BASIC = 0

# Enemy default health
ENEMY_BASIC_HEALTH = 1

# Enemy default velocity ranges
ENEMY_BASIC_VELOCITY_X = (0, 0)
ENEMY_BASIC_VELOCITY_Y = (-3, -1)

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
        if(type == ENEMY_BASIC):
            return  ENEMY_BASIC_HEALTH
        else:
            return ENEMY_BASIC_HEALTH
        
    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*ENEMY_BASIC_VELOCITY_X), random.uniform(*ENEMY_BASIC_VELOCITY_Y)
    
# Obstacle class

# List of obstacles currently on screen
obstacle_list = []

# Obstacle types
OBSTACLE_BASIC = 0

# Obstacle default health values
OBSTACLE_BASIC_HEALTH = 1

# Obstacle default velocity ranges
OBSTACLE_BASIC_VELOCITY_X = (0, 0)
OBSTACLE_BASIC_VELOCITY_Y = (-5, -2)

class Obstacle(Entity):
    def __init__(self, type):
        x, y = Obstacle.get_coordinates_from_type(type)
        velocity_x, velocity_y = Obstacle.get_velocity_from_type(type)
        super().__init__(x, y, velocity_x, velocity_y)
        self.type = type
        self.health = Obstacle.get_health_from_type(type)

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, 50, 50, arcade.color.ARMY_GREEN, 0)

    @staticmethod
    def get_health_from_type(type):
        if(type == OBSTACLE_BASIC):
            return  OBSTACLE_BASIC_HEALTH
        else:
            return OBSTACLE_BASIC_HEALTH
        
    @staticmethod
    def get_coordinates_from_type(type):
        return random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10
    
    @staticmethod
    def get_velocity_from_type(type):
        return random.uniform(*OBSTACLE_BASIC_VELOCITY_X), random.uniform(*OBSTACLE_BASIC_VELOCITY_Y)
    
# Collectable class

# List of collectables currently on screen
collectable_list = []

# Collectable types
COLLECTABLE_BASIC = 0

# Collectable default velocity ranges
COLLECTABLE_BASIC_VELOCITY_X = (0, 0)
COLLECTABLE_BASIC_VELOCITY_Y = (-3, -1)

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
        return random.uniform(*COLLECTABLE_BASIC_VELOCITY_X), random.uniform(*COLLECTABLE_BASIC_VELOCITY_Y)
    
# Bullet class

# List of bullets currently on screen
bullet_list = []

# Bullet types
BULLET_PLAYER_BASIC = 0
BULLET_ENEMY_BASIC = 100

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