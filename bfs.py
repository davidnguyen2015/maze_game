from collections import deque

class BFS:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.path = []
        self.find_path()

    def find_path(self):
        queue = deque([self.start])
        came_from = {self.start: None}
        while queue:
            current = queue.popleft()
            if current == self.goal:
                self.path = self.reconstruct_path(came_from, current)
                return
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] != '#':
                neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_next_move(self, current_pos):
        if not self.path:
            return None
        current_index = self.path.index(current_pos)
        if current_index + 1 < len(self.path):
            return self.path[current_index + 1]
        return None