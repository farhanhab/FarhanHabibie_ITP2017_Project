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

#Global variables for the colours
lives = 3
direction = 1
  
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
 
        #Speed vectors of the player
        self.change_x = 0
        self.change_y = 0

        #Attributes that will be used later to help player shoot in correct directions
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        
        self.level = None
 
    def update(self):
        """ Move the player. """

        #Gravity
        self.calc_grav()
 
        #Speed of the player in x directions       
        self.rect.x += self.change_x
 
        #Collisions with the platforms at the side
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                
                self.rect.left = block.rect.right
 
        #Set speed of player in the y directions
        self.rect.y += self.change_y
 
        #Collisions with platforms at the top and bottom       
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
        """ Constructor to create the image of the enemy """
        
        self.image = pygame.Surface([40,60])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.y = 0

    def changedirection(self):
        #Function used so that the player should be able to move down
        if self.rect.x == 700: 
            moveDown()
            self.rect.x -= 12
        elif self.rect.x < 0:
            moveDown()

    def update(self):

        #Sets the rightward speed of the player
        self.rect.x += 2

        #If the enemy is at the edge of the screen
        if self.rect.x == 700:
            #Move down by 20
            self.rect.y += 20
            #Set speed to opposite direction
            self.rect.x -= self.rect.x - 1
        if self.rect.x < 0:
            self.rect.y += 12
            self.rect.x +=12

class PUP(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        """ Constructer to create the image of the power up """

        self.image = pygame.Surface([20,20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        

class Bullet(pygame.sprite.Sprite):

    def __init__(self,player_x, player_y, player_left, player_right, player_up, player_down):
        """ Constructor, create the image of the bullet. """
        super().__init__()
        #Dimensions
        self.image = pygame.Surface([10, 10])
        #Colour
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #Sets of attribuets that let player shoot in respective directions
        self.left = player_left 
        self.right = player_right
        self.up = player_up
        self.down = player_down
        self.rect.x=player_x + 20
        self.rect.y=player_y + 20
              
    def update(self):
        """ Automatically called when we need to move the block. """
        #Sets of conditions that let player shoot in the respective directions 
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
        #The parameters set to draw the platform
        self.image = pygame.Surface([width, height])
        #Sets the colour of the platform to green
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
 
class Level(object):
    
 
    def __init__(self, player):
        #Puts the platform list as a spritegroup
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

    #Setting a boolean condition false before triggering start screen
    start_screen = False

    #While condition to trigger the start screen
    while start_screen == False:
        #Start by filling the screen black
        screen.fill(BLACK)
        #Initialising the font to write the text in
        myfont = pygame.font.SysFont('freesansbold.ttf',20)
        font = pygame.font.SysFont('freesansbold.ttf',20)
        #Assigns LeftText a way of rendering the font
        LeftText = myfont.render('Click any button to start the game',2, WHITE)
        #Assigns MidText a way of rendering the font
        MidText = font.render('Arrow keys are for moving',2,WHITE)
        #Assigns RightText a way of rendering the font
        RightText = font.render('Shoot bullets with space',2,WHITE)
        #Drawing LeftText, MidText and RightText onto the screen
        screen.blit(LeftText,(300,300))
        screen.blit(MidText,(40,300))
        screen.blit(RightText,(560,300))
        #Refreshes the screen
        pygame.display.flip()
        #Creates an event where if any key is pressed
        for event in pygame.event.get():
            #It will trigger the start screen function making it true
            #Works for any key to be pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_screen = True
                    if event.key == pygame.K_RIGHT:
                        start_screen = True
                    if event.key == pygame.K_LEFT:
                        start_screen = True
                    if event.key == pygame.K_UP:
                        start_screen = True
                    if event.key == pygame.K_DOWN:
                        start_screen = True
                        
                    
    
    pygame.display.set_caption("Farhans Game")
 
    # Create the player
    player = Player()

    #Create the enemy
    enemy = Enemy()

    #Create the powerup
    powerup = PUP()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
    powerup_list = [1]
    powerup_list.append(powerup)
 
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    #Where the player is drawn onto the sreen 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    

    #Initialising all the pygame sprite groups that are needed
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    all_sprites_group = pygame.sprite.Group()
    AI_bullet_list = pygame.sprite.Group()
    powerup_list = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()

    
    #Where the powerup is drawn onto the screen
    powerup.rect.x = 100
    powerup.rect.y = 100
    powerup_group.add(powerup)

    #Where the enemy is drawn onto the screen
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

            #When a key is pressed. Specifically used for the space to shoot bullets
            pressed=pygame.key.get_pressed()

            #If there is a key pressed event
            if event.type == pygame.KEYDOWN:
                #If the left key is pressed
                if event.key == pygame.K_LEFT:
                    #Call the players go left function
                    player.go_left()
                    #Set of boolean conditions for the player to be able to shoot in the correct direction
                    player.left = True
                    player.right = False
                    player.up = False
                    player.down = False

                    #If the right key is pressed
                if event.key == pygame.K_RIGHT:
                    #Call the players go right function
                    player.go_right()
                    #Set of boolean conditions for the player to be able to shoot in the correct direction
                    player.right = True
                    player.left = False
                    player.up = False
                    player.down = False
                
                    #If the up key is pressed
                if event.key == pygame.K_UP:
                    #Call the players jump function
                    player.jump()
                    #Set of boolean conditions for the player to be able to shoot in the correct direction
                    player.up = True
                    player.left = False
                    player.right = False
                    player.down = False

                    #If the space key is pressed
                if pressed[pygame.K_SPACE]:
                    #Call the bullet
                    bullet = Bullet(player_x, player_y, player_left, player_right, player_up, player_down)
                    #Add bullet into the sprite group
                    all_sprites_group.add(bullet)
                    #Add bullet into the bullet group
                    bullet_group.add(bullet)
                    #This is the bullets speed in the y direction
                    bullet.rect.y -= 6
                    
                 #If the event type is the player releasing the key,
            if event.type == pygame.KEYUP:
                #Stop player movement if left is lifted
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                    #Stop player movement if right is lifted
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
     
        #This block of code is needed for the bullet to work
        player_x = player.rect.x   
        player_y = player.rect.y   
        player_left = player.left 
        player_right = player.right 
        player_up = player.up 
        player_down = player.down
        #Updates the active sprite list
        active_sprite_list.update()

        #Update the groups
        current_level.update()
        bullet_group.update()
        all_sprites_group.update()
        powerup_group.update()

        #Checks the side the player is on
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        
        if player.rect.left < 0:
            player.rect.left = 0

        #Drawing all the groups on the screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        all_sprites_group.draw(screen)
        powerup_group.draw(screen)

        #Initialising the powerup variables
        powerup_on = False
        powerup_timer = 0
        powerup_collide = False

        #Collision between bullet and enemy
        for bullet in bullet_group:
            hit_enemy = pygame.sprite.spritecollide(bullet, enemy_group, True)

            #If a bullet hits an enemy
            for bullet in hit_enemy:
                #Increase the score by 1
                score += 1
                #print(score)

        #Collision for player and powerup
        for powerup in powerup_group: 
            player_p = pygame.sprite.spritecollide(player, powerup_group, True)
            
        #Condition to activate powerup
        if player_p:
            powerup_on = True

        #When powerup is activated
        if powerup_on == True:
            #Increase the speed of the player by 3 
            player.change_x += 3
            #Starts the powerup timer
            powerup_timer = 0

        #Increments the powerup timer by the amount of frames per second
        powerup_timer += 1

        #Function for ending the powerup timer
        if powerup_timer%300 == 0:
            #Sets the players speed back to normal
            player.change_x = player.change_x
            #Turns the powerup off
            powerup_on = False
                
        
        font = pygame.font.Font(None, 30)
        #Sets font

        health_bar_outline = pygame.draw.rect(screen, WHITE, [95, 25, 110, 40])
        #Draws health bar outline

        health_bar = pygame.draw.rect(screen, RED, [100, 30, 100, 30])
        #Draws health bar

        screen.blit(font.render("HEALTH", True, WHITE), [10, 35])
        #Writes the healthbar text

        score_text = font.render("Score: " + str(score), True, WHITE)
        #Sets how to draw score

        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        #Sets how to draw lives

        screen.blit(score_text, [400,40])
        #Draws the score text at this location

        screen.blit(lives_text, [600,40])
        #Draws lives text at this location


        pygame.display.flip()

        clock.tick(60)
 
   
    pygame.quit()
 
if __name__ == "__main__":
    main()
