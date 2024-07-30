# display.py

import pygame

def draw_maze(surface, maze, cell_size, offset_y=0):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size + offset_y, cell_size, cell_size)
            if cell == '#':
                pygame.draw.rect(surface, (0, 0, 0), rect)
            elif cell == ' ':
                pygame.draw.rect(surface, (255, 255, 255), rect)
            elif cell == 'P':
                pygame.draw.rect(surface, (255, 255, 255), rect)

def draw_mouse(surface, mouse_pos, cell_size, offset_y=0):
    mouse_image = pygame.image.load("mouse.png")
    mouse_image = pygame.transform.scale(mouse_image, (cell_size, cell_size))
    surface.blit(mouse_image, (mouse_pos[0] * cell_size, mouse_pos[1] * cell_size + offset_y))

def draw_pizza(surface, pizza_pos, cell_size, offset_y=0):
    pizza_image = pygame.image.load("pizza.png")
    pizza_image = pygame.transform.scale(pizza_image, (cell_size, cell_size))
    surface.blit(pizza_image, (pizza_pos[0] * cell_size, pizza_pos[1] * cell_size + offset_y))

def draw_fireworks(surface, fireworks, offset_y=0):
    for firework in fireworks:
        pygame.draw.circle(surface, firework['color'], (firework['pos'][0], firework['pos'][1] + offset_y), firework['radius'])

def draw_text(surface, text, x, y, size):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, (0, 0, 0))
    surface.blit(text_surface, (x, y))
