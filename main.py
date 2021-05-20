import pygame
import math
import random
import sys

# Game Function
def game():

    # Initializing the pygame
    pygame.init()

    # Creating game window
    WIDTH = 800
    HEIGHT = 600
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Tracks game time
    game_clock = pygame.time.Clock()

    # Background Image
    game_background = pygame.transform.scale(pygame.image.load('./background_image.png'), (WIDTH, HEIGHT))

    # Background Music
    pygame.mixer.music.load('./background_music.wav')
    pygame.mixer.music.play(-1)

    # Adding title and icon on top of game window
    pygame.display.set_caption("Space Invaders (CO PROJECT)")
    game_icon = pygame.image.load('./game_icon.png')
    pygame.display.set_icon(game_icon)

    # Player data
    player_IMAGE = pygame.image.load('./player_image.png')
    player_X = WIDTH-WIDTH/2-player_IMAGE.get_width()/2
    player_Y = HEIGHT-100
    player_X_change = 0

    # Enemy data
    enemy_IMAGE = []
    enemy_X = []
    enemy_Y = []
    enemy_X_change = []
    enemy_Y_change = []
    number_of_enemies = 6

    # Declaring data for every enemy
    for i in range(number_of_enemies):
        enemy_IMAGE.append(pygame.image.load('./enemy_image.png'))
        enemy_X.append(random.randint(0, WIDTH-enemy_IMAGE[i].get_width()))
        enemy_Y.append(random.randint(50, 150))
        enemy_X_change.append(8)
        enemy_Y_change.append(40)

    # Bullet data
    bullet_IMAGE = pygame.image.load('./bullet_image.png')
    bullet_X = 0
    bullet_Y = HEIGHT-100
    bullet_Y_change = 20
    bullet_status = "ready"

    # Score text
    game_score = 0
    game_score_font = pygame.font.Font('./Valentime.otf', 32)
    game_scoreX = 10
    game_scoreY = 10

    # Game Over text
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_restart_font = pygame.font.Font('freesansbold.ttf', 32)

    # Function to display bullet
    def bullet(x, y):
        game_screen.blit(bullet_IMAGE, (x+16, y+10))

    # Function to display player
    def player(x, y):
        game_screen.blit(player_IMAGE, (x, y))

    # Function to display enemies
    def enemy(x, y, i):
        game_screen.blit(enemy_IMAGE[i], (x, y))

    # Function to check for a collision between a bullet and an enemy
    def is_Collision(enemy_X, enemy_Y, bullet_X, bullet_Y):
        collide = math.sqrt((math.pow((enemy_X-bullet_X), 2)) + (math.pow((enemy_Y-bullet_Y), 2)))
        if collide < 27:
            return True
        else:
            return False

    # Function to display score
    def show_score(x, y):
        game_score_value = game_score_font.render("Score : " + str(game_score), True, (255, 255, 255))
        game_screen.blit(game_score_value, (x, y))

    # Function to display game over text
    def game_over_text():
        game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
        game_restart_text = game_restart_font.render("Press Q to Quit or P to Restart", True, (255, 255, 255))
        game_screen.blit(game_over_text, (WIDTH/2- game_over_text.get_width()/2, 250))
        game_screen.blit(game_restart_text, (WIDTH/2-game_restart_text.get_width()/2, 330))

    # Function to display a boundary line which enemies wants to cross
    def boundary_line():
        pygame.draw.line(game_screen, (255, 255, 255), (0, player_Y-5), (WIDTH, player_Y-5))

    # Frames per second at which game will be played
    FPS = 60

    # Variable to execute game loop
    run = True

    # Game Loop
    while run:

        # Maintaining Frames per second by tracking game time
        game_clock.tick(FPS)

        # Filling game screen with black colour over previous frame
        game_screen.fill((0, 0, 0))

        # Adding background Image to game screen
        game_screen.blit(game_background, (0, 0))

        # Calling boundary_line() function
        boundary_line()

        # Checks for any user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_X_change = -10
                elif event.key == pygame.K_RIGHT:
                    player_X_change = 10
                elif event.key == pygame.K_SPACE:
                    if bullet_status == "ready":
                        # Plays a sound of bullet firing
                        bullet_firing_sound = pygame.mixer.Sound('./bullet_sound.wav')
                        bullet_firing_sound.play()
                        bullet_status = "fire"
                        bullet_X = player_X
                        # Calling fire_bullet() function
                        bullet(bullet_X, bullet_Y)
                elif event.key == pygame.K_q:
                    run = False
                elif event.key == pygame.K_p:
                    game()

            # if key has been released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_X_change = 0
                elif event.key == pygame.K_RIGHT:
                    player_X_change = 0

        # Player movement
        player_X += player_X_change

        # Creating bounds for player's movement
        if player_X <= 0:
            player_X = 0
        elif player_X >= WIDTH-player_IMAGE.get_width():
            player_X = WIDTH-player_IMAGE.get_width()

        # Enemy movement
        for i in range(number_of_enemies):
            enemy_X[i] += enemy_X_change[i]

            # Creating bounds for enemy's movement and increasing enemy's Y-coordinate every time it hits extreme X-coordinate of game screen
            if enemy_X[i] >= WIDTH-enemy_IMAGE[i].get_width():
                enemy_X_change[i] = -8
                enemy_Y[i] += enemy_Y_change[i]
            elif enemy_X[i] <= 0:
                enemy_X_change[i] = 8
                enemy_Y[i] += enemy_Y_change[i]

            # Game Over when any enemy crosses the boundary line
            if enemy_Y[i] >= player_Y-enemy_IMAGE[i].get_width()-4:
                for j in range(number_of_enemies):
                    enemy_Y[j] = 2000
                game_over_text()
                break

            # Collision
            collision = is_Collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
            if collision:
                # Plays a sound of collision when a bullet hits an enemy
                collision_noise = pygame.mixer.Sound('./collision_sound.wav')
                collision_noise.play()
                bullet_Y = HEIGHT-100
                bullet_status = "ready"
                # Increment score by 1 for every collision
                game_score += 1
                # Reswapn an enemy 
                enemy_X[i] = random.randint(0, WIDTH-enemy_IMAGE[i].get_width())
                enemy_Y[i] = random.randint(50, 150)

            # Calling enemy() function
            enemy(enemy_X[i], enemy_Y[i], i)

        # Reloading a bullet
        if bullet_Y <= 0:
            bullet_Y = HEIGHT-100
            bullet_status = "ready"

        # Shooting a bullet
        if bullet_status == "fire":
            # Calling fire_bullet() function
            bullet(bullet_X, bullet_Y)
            bullet_Y -= bullet_Y_change

        # Calling player() function
        player(player_X, player_Y)

        # Calling show_score() function
        show_score(game_scoreX, game_scoreY)

        # Updating Game Screen 
        pygame.display.update()

    # Uninitialize pygame modules and stops the game
    pygame.quit()
    sys.exit()

# Calling game() function
game()  
