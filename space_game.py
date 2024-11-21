# This is a very basic skeleton we can build on for creating the game.
# It defines an Entity class that contains coordinates and velocities.
# Every "frame" (one second to make it easier to read) coordinates of
# each Entity are updated and printed to console.
#
# Next steps might be to implement different classes that extend the
# Entity class, figure out an efficient way to determine when two
# Entities are touching, implement functions to create new Entities,
# implement methods for the different Entity types that determine how
# they behave, etc.
# 
# Program currently runs forever, use CTRL+C to stop it.

import time

class Entity:
    def __init__(self, x, y, velocityX, velocityY):
        self.x = x
        self.y = y
        self.velocityX = velocityX
        self.velocityY = velocityY

    def update(self):
        self.x += self.velocityX
        self.y += self.velocityY

    # placeholder function to view entity information
    def print(self, id):
        print("Entity " + str(id) + " at (" + str(self.x) + ", " + str(self.y) + \
            ") with velocity (" + str(self.velocityX) + ", " + str(self.velocityY) + ")")
        
def main():
    # Create an array of Entities for testing purposes
    entityList = []
    entityList.append(Entity(25, 25, 1, -1))
    entityList.append(Entity(23, 44, 5, 4))
    entityList.append(Entity(0, 78, 3, -1))
    entityList.append(Entity(45, 54, -3, 1))
    entityList.append(Entity(77, 77, -1, 1))
    
    # Game loop
    while(1):
        for index, entity in enumerate(entityList):
            entity.print(index)
            entity.update()
        print(". . .")
        time.sleep(1) # wait one second before printing updated values

if __name__ == "__main__":
    main()