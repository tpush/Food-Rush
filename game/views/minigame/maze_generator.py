import random
import heapq


class MazeGenerator:
    """Генерация лабиринта, используя алгоритм рекурсивного возврата."""

    def __init__(self, rows, cols):
        self.rows = rows if rows % 2 != 0 else rows + 1
        self.cols = cols if cols % 2 != 0 else cols + 1
        self.maze = [[1 for _ in range(self.cols)]
                     for _ in range(self.rows)]

    def generate(self):
        """Основной метод для генерации лабиринта."""
        stack = [(1, 1)]
        self.maze[1][1] = 0

        while stack:
            r, c = stack[-1]
            neighbors = []
            for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                nr, nc = r + dr, c + dc
                if (0 < nr < self.rows - 1 and
                        0 < nc < self.cols - 1 and self.maze[nr][nc] == 1):
                    neighbors.append((nr, nc))

            if neighbors:
                next_r, next_c = random.choice(neighbors)
                # Убираем стену между текущей и следующей ячейкой
                self.maze[r + (next_r - r) // 2][c + (next_c - c) // 2] = 0
                self.maze[next_r][next_c] = 0
                stack.append((next_r, next_c))
            else:
                stack.pop()

        # Создние входа и выхода
        self.maze[1][0] = 0
        self.maze[self.rows-2][self.cols-1] = 0

        return self.maze


class AStarPathfinder:
    """Нахождение кратчайшего пути в лабиринте с помощью алгоритма A*."""

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def find_path(self, start, end):
        """Нахождение пути от начальной точки до конечной."""
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {(r, c): float('inf')
                   for r in range(self.rows) for c in range(self.cols)}
        g_score[start] = 0
        f_score = {(r, c): float('inf')
                   for r in range(self.rows) for c in range(self.cols)}
        f_score[start] = self._heuristic(start, end)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = (g_score[neighbor] +
                                         self._heuristic(neighbor, end))
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def _heuristic(self, a, b):
        """Манхэттенское расстояние."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, pos):
        """Возвращение списка соседних проходимых ячеек."""
        r, c = pos
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < self.rows and
                    0 <= nc < self.cols and self.maze[nr][nc] == 0):
                neighbors.append((nr, nc))
        return neighbors

    def _reconstruct_path(self, came_from, current):
        """Восстановление пути от конца к началу."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
