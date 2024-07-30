# mouse.py

class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        if maze[self.y + dy][self.x + dx] != '#':
            self.x += dx
            self.y += dy

    def get_position(self):
        return (self.x, self.y)
