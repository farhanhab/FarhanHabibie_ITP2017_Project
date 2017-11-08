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

lives = 3
direction = 1

##start_screen = False
##font = pygame.font.SysFont('freesansbold.ttf',50)
##while start_screen == False:
##    screen.fill(BLACK)
##    font = pygame.font.Font(None, 50)
##    screen.blit(font.render("Press Arrow Keys to move", True, WHITE), [10,100])
##    screen.blit(font.render("Press Space to shoot", True, WHITE), [600, 100])
##    screen.blit(font.render("Press Any Key to start", True, WHITE), [300, 100])
##    pygame.display.flip()
##    for event in pygame.event.get():
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_LEFT:
##                    start_screen = True
##                if event.key == pygame.K_RIGHT:
##                    start_screen = True
##                if event.key == pygame.K_UP:
##                    start_screen = True
##                if event.key == pygame.K_DOWN:
##                    start_screen = True
##                if event.key == pygame.K_SPACE:
##                    start_screen = True
  
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

class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([40,60])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.y = 0

    def changedirection(self):
        if self.rect.x == 700: 
            moveDown()
            self.rect.x -= 12
        elif self.rect.x < 0:
            moveDown()

    def update(self):
        self.rect.x += 2
        
        if self.rect.x == 700:
            self.rect.y += 20
            self.rect.x -= self.rect.x - 1
        if self.rect.x < 0:
            self.rect.y += 12
            self.rect.x +=12

class PUP(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([20,20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        

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
        self.rect.x=player_x + 20
        self.rect.y=player_y + 20
              
    def update(self):
        """ Automatically called when we need to move the block. """
        if self.left==True:   
            self.rect.x -= 6
        if self.right==True: 
            self.rect.x += 6
        if self.up==True:    
            self.rect.y -= 6
        if self.down==True: 
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
    score = 0
 
    pygame.display.set_caption("Farhans Game")
 
    # Create the player
    player = Player()
    enemey = Enemy()
    powerup = PUP()
 
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
    AI_bullet_list = pygame.sprite.Group()
    powerup_list = pygame.sprite.Group()

    enemy = Enemy()
    enemy.rect.x = 100
    enemy.rect.y = 70
    all_sprites_group.add(enemy)
    enemy_group.add(enemy)
    


    done = False
 
    
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            pressed=pygame.key.get_pressed()

            if event.type == pygame.KEYDOWN:
                if pressed[pygame.K_LEFT]:
                    player.go_left()
                    player.left = True
                    player.right = False
                    player.up = False
                    player.down = False
                    
                if pressed[pygame.K_RIGHT]:
                    player.go_right()
                    player.right = True
                    player.left = False
                    player.up = False
                    player.down = False
                
                if pressed[pygame.K_UP]:
                    player.jump()
                    player.up = True
                    player.left = False
                    player.right = False
                    player.down = False
                    
                if pressed[pygame.K_SPACE]:
                    bullet = Bullet(player_x, player_y, player_left, player_right, player_up, player_down)
                    all_sprites_group.add(bullet)
                    bullet_group.add(bullet)
                    bullet.rect.y -= 6
                    
                 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
     

        player_x = player.rect.x   
        player_y = player.rect.y   
        player_left = player.left 
        player_right = player.right 
        player_up = player.up 
        player_down = player.down        
        active_sprite_list.update()
 
        
        current_level.update()
        bullet_group.update()
        all_sprites_group.update()
        
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        
        if player.rect.left < 0:
            player.rect.left = 0
 
        
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        all_sprites_group.draw(screen)
        

        for bullet in bullet_group:
            hit_enemy = pygame.sprite.spritecollide(bullet, enemy_group, True)

            for bullet in hit_enemy:
                score += 1
                print(score)
                

        font = pygame.font.Font(None, 30)
        health_bar_outline = pygame.draw.rect(screen, WHITE, [95, 25, 110, 40])
        health_bar = pygame.draw.rect(screen, RED, [100, 30, 100, 30])
        screen.blit(font.render("HEALTH", True, WHITE), [10, 35])
        score_text = font.render("Score: " + str(score), True, WHITE)
        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(score_text, [400,40])
        screen.blit(lives_text, [600,40])


        pygame.display.flip()

        clock.tick(60)
 
   
    pygame.quit()
 
if __name__ == "__main__":
    main()
