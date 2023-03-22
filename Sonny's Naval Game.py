import pygame
import random
import sys

# Constants
WIDTH = 800
HEIGHT = 800
ROWS = 80
COLS = 80
TILE_SIZE = WIDTH // COLS
ISLAND_COUNT = 10
AI_SHIP_COUNT = 3

# Colors
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonny's Naval Game")

# Game clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)


class Island:
    def __init__(self, x, y, size, port, resources):
        self.x = x
        self.y = y
        self.size = size
        self.port = port
        self.resources = resources

    def tiles(self):
        island_tiles = []
        for j in range(-self.size, self.size + 1):
            for k in range(-self.size, self.size + 1):
                island_tiles.append((self.x + j, self.y + k))
        return island_tiles

    def port_tile(self):
        return (self.x + self.port[0], self.y + self.port[1])


class Ship:
    def __init__(self, x, y, color, is_player=False, ai_index=None):
        self.x = x
        self.y = y
        self.color = color
        self.health = 100
        self.is_player = is_player
        self.ai_index = ai_index

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if self.is_player:
            text = font.render("You", True, WHITE)
            surface.blit(text, (self.x * TILE_SIZE + TILE_SIZE // 4, self.y * TILE_SIZE + TILE_SIZE // 4))
        else:
            text = font.render("AI Ship {}".format(self.ai_index), True, WHITE)
            surface.blit(text, (self.x * TILE_SIZE + TILE_SIZE // 4, self.y * TILE_SIZE + TILE_SIZE // 4))


class Player:
    def __init__(self):
        self.resources = {"Wood": 0, "Steel": 0, "Oil": 0, "Food": 0}

    def gather_resources(self, island):
        for resource, amount in island.resources.items():
            self.resources[resource] += amount
            island.resources[resource] = 0


def generate_islands(count):
    islands = []
    for _ in range(count):
        island_size = random.randint(1, 5)
        island_x = random.randint(island_size, COLS - island_size)
        island_y = random.randint(island_size, ROWS - island_size)
        port_x_offset = random.randint(-island_size + 1, island_size - 1)
        port_y_offset = random.randint(-island_size + 1, island_size - 1)
        resources = {"Wood": random.randint(100, 500),
                     "Steel": random.randint(100, 500),
                     "Oil": random.randint(100, 500),
                     "Food": random.randint(100, 500)}
        island = Island(island_x, island_y, island_size, (port_x_offset, port_y_offset), resources)
        islands.append(island)
    return islands


def generate_ai_ships(count, islands, player_ship):
    ai_ships = []
    for i in range(count):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            is_on_island = any([(x, y) in island.tiles() for island in islands])
            if not is_on_island and (x, y) != (player_ship.x, player_ship.y):
                break

        ai_ship = Ship(x, y, RED, is_player=False, ai_index=i + 1)
        ai_ships.append(ai_ship)
    return ai_ships


def draw_map(screen, islands, player_ship, ai_ships):
    for i in range(COLS):
        for j in range(ROWS):
            color = LIGHT_BLUE
            for island in islands:
                if (i, j) in island.tiles():
                    color = BROWN
                    break

            pygame.draw.rect(screen, color, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for island in islands:
        port_x, port_y = island.port_tile()
        pygame.draw.circle(screen, WHITE, (port_x * TILE_SIZE + TILE_SIZE // 2, port_y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)

    player_ship.draw(screen)

    for ai_ship in ai_ships:
        ai_ship.draw(screen)


def main():
    islands = generate_islands(ISLAND_COUNT)
    player_ship = Ship(COLS // 2, ROWS // 2, BLUE, is_player=True)
    ai_ships = generate_ai_ships(AI_SHIP_COUNT, islands, player_ship)
    player = Player()

    running = True
    while running:
        screen.fill(BLACK)
        draw_map(screen, islands, player_ship, ai_ships)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                new_x = player_ship.x
                new_y = player_ship.y

                if event.key == pygame.K_w:
                    new_y = max(0, player_ship.y - 1)
                elif event.key == pygame.K_a:
                    new_x = max(0, player_ship.x - 1)
                elif event.key == pygame.K_s:
                    new_y = min(ROWS - 1, player_ship.y + 1)
                elif event.key == pygame.K_d:
                    new_x = min(COLS - 1, player_ship.x + 1)

                is_on_island = any([(new_x, new_y) in island.tiles() for island in islands])
                if not is_on_island:
                    player_ship.move(new_x - player_ship.x, new_y - player_ship.y)

        for island in islands:
            if (player_ship.x, player_ship.y) == island.port_tile():
                player.gather_resources(island)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()


