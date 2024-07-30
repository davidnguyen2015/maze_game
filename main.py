import pygame
import sys
import random
import time
from maze_generator import generate_maze
from display import draw_maze, draw_mouse, draw_pizza, draw_fireworks, draw_text
from mouse import Mouse
from dijkstra import Dijkstra
from bellman_ford import BellmanFord
from bfs import BFS
from dfs import DFS

#init game
pygame.init()

# constants
WIDTH, HEIGHT = 1100, 900
CELL_SIZE = 20
INFO_HEIGHT = 100
FPS = 10
SCORE_FILE = "scores.txt"

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
    global maze, pizza_pos, mouse, fireworks, start, goal, start_time, step, won, win_time, ai_mode, ai_menthod, ai, elapsed_time
    maze, pizza_pos, mouse, fireworks, start, goal = init_game()
    start_time = time.time()
    step = 0
    won = False
    win_time = None
    ai_mode = False
    ai_menthod = ''
    ai = None
    elapsed_time = 0

def save_score(time_taken, step):
    with open(SCORE_FILE, "a") as file:
        #print(step)
        file.write(f"Time: {time_taken:.2f} s, Step: {step}\n")

def trigger_fireworks(pos):
    for _ in range(10):
        fireworks.append({
            'pos': (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2),
            'color': pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            'radius': random.randint(2, 10),
        })

def main():
    # Initialize sound
    pygame.mixer.init()
    eat_sound = pygame.mixer.Sound("eat.mp3")

    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
    pygame.display.set_caption("Mouse Maze")

    maze, pizza_pos, mouse, fireworks, start, goal = init_game()
    start_time = time.time()
    step = 0

    clock = pygame.time.Clock()
    paused = False
    won = False
    win_time = None
    ai_mode = False
    ai_menthod = ''
    ai = None
    elapsed_time = 0

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

                #1 -> dijkstra
                #2 -> bellman_ford
                #3 -> bfs
                #4 -> dfs
                if event.key == pygame.K_1:
                    ai_mode = not ai_mode
                    ai_menthod = "Dijkstra"
                    if ai_mode:
                        ai = Dijkstra(maze, start, goal)
                if event.key == pygame.K_2:
                    ai_mode = not ai_mode
                    ai_menthod = "Bellman Ford"
                    if ai_mode:
                        ai = BellmanFord(maze, start, goal)
                if event.key == pygame.K_3:
                    ai_mode = not ai_mode
                    ai_menthod = "Breadth-First Search"
                    if ai_mode:
                        ai = BFS(maze, start, goal)
                if event.key == pygame.K_4:
                    ai_mode = not ai_mode
                    ai_menthod = "Depth-First Search"
                    if ai_mode:
                        ai = DFS(maze, start, goal)
        
        if not paused:
            # Update time only if not paused
            elapsed_time = time.time() - start_time

            if not won:
                if ai_mode and ai:
                    next_move = ai.get_next_move((mouse.x, mouse.y))
                    if next_move:
                        dx, dy = next_move[0] - mouse.x, next_move[1] - mouse.y
                        mouse.move(dx, dy, maze)
                        step += 1
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        step += 1
                        mouse.move(0, -1, maze)
                    if keys[pygame.K_DOWN]:
                        step += 1
                        mouse.move(0, 1, maze)
                    if keys[pygame.K_LEFT]:
                        step += 1
                        mouse.move(-1, 0, maze)
                    if keys[pygame.K_RIGHT]:
                        step += 1
                        mouse.move(1, 0, maze)

                # Check if mouse has reached pizza
                if (mouse.x, mouse.y) == (pizza_pos[0], pizza_pos[1]):
                    eat_sound.play()
                    trigger_fireworks(mouse.get_position())
                    won = True

            # Update fireworks
            fireworks = [f for f in fireworks if f['radius'] > 0]
            for firework in fireworks:
                firework['radius'] -= 0.1

        # Draw everything
        screen.fill((255, 255, 255))
        # Draw information panel
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, INFO_HEIGHT))
        #print(f'Time: {elapsed_time:.1f}s')
        draw_text(screen, f'Time: {elapsed_time:.1f}s' if not paused else 'Paused', 10, 10, 30)
        draw_text(screen, f'Step: {step}', 10, 50, 30)
        
        # Draw the game area
        draw_maze(screen, maze, CELL_SIZE, offset_y=INFO_HEIGHT)
        draw_mouse(screen, mouse.get_position(), CELL_SIZE, offset_y=INFO_HEIGHT)
        draw_pizza(screen, pizza_pos, CELL_SIZE, offset_y=INFO_HEIGHT)
        draw_fireworks(screen, fireworks, offset_y=INFO_HEIGHT)

        if won:
            draw_text(screen, "You Won!", WIDTH // 2, INFO_HEIGHT // 2, 55)
            win_time = time.time()
            save_score(elapsed_time, step)
            pygame.display.flip()
            pygame.time.wait(3000)
            reset_game()
        else:
            if paused:
                draw_text(screen, "Paused", WIDTH // 2, INFO_HEIGHT // 2, 55)
            else:
                draw_text(screen, ai_menthod, WIDTH // 2, INFO_HEIGHT // 2, 55)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()