import arcade

# these will be our constants that we can establish however I left the player speed and bullet speed as variables
# so that we can possibly alter them with buffs and debuff we want to create 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
playerSpeed = 5
bulletSpeed = 7

class SpaceGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Game")
        self.player = None
        self.player_list = None
        self.bullet_list = None
        
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
        self.score = 0  
        self.game_over = False  
        self.wave = 1  
         

        # This is our player I tried to find different sprites but this is what I have for now 
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 50
        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        
        # This will display the score and text for our game
        arcade.draw_text(f"Score: {self.score}", 10, 570, arcade.color.WHITE, 20)
        arcade.draw_text(f"Wave: {self.wave}", SCREEN_WIDTH - 100, 570, arcade.color.WHITE, 20)
    
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
    
    #Updates button press on release so that we dont continue moving
    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0
        elif key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0

    def update(self, delta_time):
        if self.game_over:
            return  

        self.player_list.update()
        self.bullet_list.update()

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

def main():
    game = SpaceGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()