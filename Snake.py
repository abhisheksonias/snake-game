import pygame, sys, time, random

pygame.font.init()

#snake speed (Difficulty Level)
speed = 15

#error Check
error = pygame.init()

if error[1] > 0:
    print(f'[!] Had {error[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('Game successfully initialised')
    
# Display Setup
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake game")

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
yellow = pygame.Color(255, 255, 0)
blue = pygame.Color(0, 0, 255)

# frame rate controller
fps_controller = pygame.time.Clock()

# Snake properties
snake_position = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

    # Function to display "Game Over" message
def game_over():
    scary_font = pygame.font.SysFont('chiller', 90)  # Change to a scary font name available on your system
    game_over_surface = scary_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    
    # Use a scary font to render a snake symbol
    snake_symbol_font = pygame.font.SysFont('chiller', 300)  # Adjust font size as needed
    snake_symbol_surface = snake_symbol_font.render('S', True, white)
    snake_symbol_rect = snake_symbol_surface.get_rect()
    snake_symbol_rect.midtop = (width / 2, height / 2)
    
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(snake_symbol_surface, snake_symbol_rect)
    
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()
    
# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width/10, 15)
    else:
        score_rect.midtop = (width/2, height/1.25)
    screen.blit(score_surface, score_rect)
    pygame.display.update()    
    
# Function to draw the snake
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, yellow, (segment[0], segment[1], 10, 10))

# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
        
    # Update the snake body
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_pos[0] and snake_position[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
        
        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (width//10)- 20) * 10, random.randrange(1, (height//10)-20 ) * 10]
        food_spawn = True
        
        

    # Game Over conditions
    # Getting out of bounds
    if snake_position[0] < 10 or snake_position[0] > width-20:
        game_over()
    if snake_position[1] < 10 or snake_position[1] > height-20:
        game_over()
        
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
                      
    # Draw background
    screen.fill(blue)

    # Draw border
    pygame.draw.rect(screen, red, (0, height - 10, width, 10))  # Bottom
    pygame.draw.rect(screen, red, (0, 0, width, 10))  # Top
    pygame.draw.rect(screen, red, (0, 0, 10, height))  # Left
    pygame.draw.rect(screen, red, (width - 10, 0, 10, height))  # Right

    # Draw snake
    draw_snake(snake_body)

    # Draw food
    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    show_score(1, white, 'consolas', 20)
    
    # Update display
    pygame.display.flip()
    
    # Control the game speed
    fps_controller.tick(speed)
