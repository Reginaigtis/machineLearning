import pygame
import random

# Настройки экрана
WIDTH = 800
HEIGHT = 600
FPS = 30

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DBSCAN")
clock = pygame.time.Clock()

# Основные цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)  
COLORS = [GREEN, YELLOW, RED]

# Список точек
points = []
flags = {}  # Флаги для точек
clusters = {}


def draw_points():
    for point in points:
        if clusters.get(point) == -1:  # Если точка является шумовой
            color = GREY
        elif not flags.get(point):  # Если точка еще не окрашена флажком
            color = BLACK
        else:
            color = flags[point]
        pygame.draw.circle(screen, color, point, 6)


def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def dbscan(points, eps=50, min_samples=3):
    cluster_id = 0
    visited = set()
    noise = []

    def expand_cluster(point, neighbor_pts):
        nonlocal cluster_id

        cluster_id += 1
        cluster = [point]
        while neighbor_pts:
            current_point = neighbor_pts.pop()
            if current_point in visited:
                continue
            visited.add(current_point)
            neighbors = [p for p in points if distance(current_point, p) <= eps]
            if len(neighbors) >= min_samples:
                neighbor_pts.extend([n for n in neighbors if n not in neighbor_pts])
            cluster.append(current_point)
        return cluster

    for point in points:
        if point in visited:
            continue
        visited.add(point)
        neighbors = [p for p in points if distance(point, p) <= eps]
        if len(neighbors) < min_samples:
            noise.append(point)
        else:
            cluster = expand_cluster(point, neighbors)
            for c in cluster:
                clusters[c] = cluster_id

    for n in noise:
        clusters[n] = -1  # Шумовые точки помечаем как -1


def assign_random_flags():
    for point in points:
        flags[point] = random.choice(COLORS)


running = True
eps = 50
min_samples = 3
while running:
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            points.append(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                assign_random_flags()  # Присваиваем флажки
                dbscan(points, eps=eps, min_samples=min_samples)
            elif event.key == pygame.K_BACKSPACE:
                if points:
                    del points[-1]
                    flags.clear()
                    clusters.clear()
                    dbscan(points, eps=eps, min_samples=min_samples)
            elif event.key == pygame.K_UP:
                eps += 10
            elif event.key == pygame.K_DOWN:
                eps -= 10
            elif event.key == pygame.K_LEFT:
                min_samples -= 1
            elif event.key == pygame.K_RIGHT:
                min_samples += 1
            dbscan(points, eps=eps, min_samples=min_samples)

    screen.fill(WHITE)
    draw_points()
    pygame.display.flip()

pygame.quit()