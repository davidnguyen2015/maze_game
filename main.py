# main.py

import pygame
import sys
import random
import time
from maze_generator import generate_maze
from display import draw_maze, draw_mouse, draw_pizza, draw_fireworks, draw_text
from mouse import Mouse
from ai import AI

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
INFO_HEIGHT = 100
FPS = 10

# Initialize sound
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
pygame.display.set_caption("Mouse Maze")

def init_game():
    maze_width = WIDTH // CELL_SIZE
    maze_height = HEIGHT // CELL_SIZE
    maze, pizza_pos = generate_maze(maze_width, maze_height)

    start = (1, 1)
    goal = (maze_width // 2, maze_height // 2)
    mouse = Mouse(start[0], start[1])

    fireworks = []
    return maze, pizza_pos, mouse, fireworks, start, goal

def reset_game():
    global maze, pizza_pos, mouse, fireworks, start, goal, start_time, path_length, won, win_time, ai_mode, ai
    maze, pizza_pos, mouse, fireworks, start, goal = init_game()
    start_time = time.time()
    path_length = 0
    won = False
    win_time = None
    ai_mode = False
    ai = None

maze, pizza_pos, mouse, fireworks, start, goal = init_game()
start_time = time.time()
path_length = 0

clock = pygame.time.Clock()
paused = False
won = False
win_time = None
ai_mode = False
ai = None

def trigger_fireworks(pos):
    for _ in range(10):
        fireworks.append({
            'pos': (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2),
            'color': pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            'radius': random.randint(2, 10),
        })

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_a:
                ai_mode = not ai_mode
                if ai_mode:
                    ai = AI(maze, start, goal)
    
    if not paused:
        # Update time only if not paused
        elapsed_time = time.time() - start_time

        if not won:
            if ai_mode and ai:
                next_move = ai.get_next_move((mouse.x, mouse.y))
                if next_move:
                    dx, dy = next_move[0] - mouse.x, next_move[1] - mouse.y
                    mouse.move(dx, dy, maze)
                    path_length += 1
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    path_length += 1
                    mouse.move(0, -1, maze)
                if keys[pygame.K_DOWN]:
                    path_length += 1
                    mouse.move(0, 1, maze)
                if keys[pygame.K_LEFT]:
                    path_length += 1
                    mouse.move(-1, 0, maze)
                if keys[pygame.K_RIGHT]:
                    path_length += 1
                    mouse.move(1, 0, maze)

            # Check if mouse has reached pizza
            if (mouse.x, mouse.y) == (pizza_pos[0], pizza_pos[1]):
                eat_sound.play()
                trigger_fireworks(mouse.get_position())
                won = True
                win_time = time.time()
                pygame.time.wait(2000)  # Pause for 2 seconds to show fireworks
                reset_game()

        # Update fireworks
        fireworks = [f for f in fireworks if f['radius'] > 0]
        for firework in fireworks:
            firework['radius'] -= 0.1

    # Draw everything
    screen.fill((255, 255, 255))
    # Draw information panel
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, INFO_HEIGHT))
    draw_text(screen, f'Time: {elapsed_time:.2f}s' if not paused else 'Paused', 10, 10, 30)
    draw_text(screen, f'Length: {path_length}', 10, 50, 30)
    
    if paused:
        draw_text(screen, "Paused", WIDTH // 2, INFO_HEIGHT // 2, 55)
    
    if won:
        draw_text(screen, "You Won!", WIDTH // 2, INFO_HEIGHT // 2 - 50, 55)
        if time.time() - win_time < 3:  # Show maze blinking effect for 3 seconds
            if int((time.time() - win_time) * 5) % 2 == 0:  # Blinking effect
                draw_maze(screen, [[' '] * len(maze[0]) for _ in range(len(maze))], CELL_SIZE, offset_y=INFO_HEIGHT)
    
    # Draw the game area
    draw_maze(screen, maze, CELL_SIZE, offset_y=INFO_HEIGHT)
    draw_mouse(screen, mouse.get_position(), CELL_SIZE, offset_y=INFO_HEIGHT)
    draw_pizza(screen, pizza_pos, CELL_SIZE, offset_y=INFO_HEIGHT)
    draw_fireworks(screen, fireworks, offset_y=INFO_HEIGHT)

    pygame.display.flip()
    clock.tick(FPS)
