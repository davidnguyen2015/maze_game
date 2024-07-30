import random

def generate_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]

    def in_bounds(x, y):
        return 0 < x < width - 1 and 0 < y < height - 1

    def is_valid(x, y):
        return in_bounds(x, y) and maze[y][x] == '#'

    def carve_path(x, y):
        maze[y][x] = ' '
        directions = [(0, -2), (0, 2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                maze[ny][nx] = ' '
                maze[y + dy // 2][x + dx // 2] = ' '
                carve_path(nx, ny)

    carve_path(1, 1)
    
    def create_paths_from_corners():
        corners = [(1, 1), (1, height - 2), (width - 2, 1), (width - 2, height - 2)]
        center_x, center_y = width // 2, height // 2

        for cx, cy in corners:
            x, y = cx, cy
            while x != center_x or y != center_y:
                if x < center_x:
                    x += 1
                elif x > center_x:
                    x -= 1
                if y < center_y:
                    y += 1
                elif y > center_y:
                    y -= 1
                maze[y][x] = ' '

    create_paths_from_corners()

    def place_pizza():
        cx, cy = width // 2, height // 2
        maze[cy][cx] = 'P'
        return (cx, cy)
    
    pizza_pos = place_pizza()
    return maze, pizza_pos
