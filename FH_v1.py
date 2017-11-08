import pygame
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

  
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
   
    def __init__(self):
        """ Constructor function """
 
        
        super().__init__()
 
        
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
 
 
        self.rect = self.image.get_rect()
 
        
        self.change_x = 0
        self.change_y = 0

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        
        self.level = None
 
    def update(self):
        """ Move the player. """
       
        self.calc_grav()
 
       
        self.rect.x += self.change_x
 
        
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                
                self.rect.left = block.rect.right
 
        
        self.rect.y += self.change_y
 
       
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
           
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35
 
        
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 4
 
        
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        
        self.change_x = -6
 
    def go_right(self):
        
        self.change_x = 6
 
    def stop(self):
        
        self.change_x = 0          

class Bullet(pygame.sprite.Sprite):

    def __init__(self,player_x, player_y, player_left, player_right, player_up, player_down):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.left = player_left 
        self.right = player_right
        self.up = player_up
        self.down = player_down
        self.rect.x=player_x + 5
        self.rect.y=player_y + 5

    def update(self):
        """ Automatically called when we need to move the block. """
        if self.left==True:   #if player is facing left, then shoot left
            self.rect.x -= 6
        if self.right==True: #if player is facing right, then shoot right
            self.rect.x += 6
        if self.up==True:    #if player is facing up, then shoot up
            self.rect.y -= 6
        if self.down==True: #if player is facing down, then shoot down
            self.rect.y += 6
 
class Platform(pygame.sprite.Sprite):
    
    def __init__(self, width, height):
       
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    
 
    def __init__(self, player):
        
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
       
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
       
 
        # Draw the background
        screen.fill(BLACK)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    
 
    def __init__(self, player):
        
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 [210, 70, 100, 200],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 


def main():

    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Farhans Game")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    all_sprites_group = pygame.sprite.Group()

    done = False
 
    
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                    player.left = True
                    
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                    player.right = True
                
                if event.key == pygame.K_UP:
                    player.jump()
                    player.up = True
                    
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player_x, player_y, player_left, player_right, player_up, player_down)
                    all_sprites_group.add(bullet)
                    bullet_group.add(bullet)
                    print("yo")
                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        for x in enemy_group:
            x.move()
        player_x = player.rect.x   
        player_y = player.rect.y   
        player_left = player.left 
        player_right = player.right 
        player_up = player.up 
        player_down = player.down        
        active_sprite_list.update()
 
        
        current_level.update()
 
        
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        
        if player.rect.left < 0:
            player.rect.left = 0
 
        
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        all_sprites_group.draw(screen) 
        
 
       
        clock.tick(60)
 
       
        pygame.display.flip()
 
   
    pygame.quit()
 
if __name__ == "__main__":
    main()
