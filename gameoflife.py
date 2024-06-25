import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

clock = pygame.time.Clock()

def gen(n):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(n)])

def adjust_positions(positions):
    all_neighbours = set()
    new_positions = set()
    for pos in positions:
        neighbours = get_neighbours(pos)
        all_neighbours.update(neighbours)
        
        neighbours = list(filter(lambda x: x in positions, neighbours)) # check for alive neighbours

        if len(neighbours) in [2, 3]:
            new_positions.add(pos)
    for pos in all_neighbours:
        neighbours = get_neighbours(pos)
        neighbours = list(filter(lambda x: x in positions, neighbours))
        if len(neighbours) == 3:
            new_positions.add(pos)

    return new_positions

def get_neighbours(pos):
    neighbour = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_col = (pos[0] + dx) % GRID_WIDTH
            new_row = (pos[1] + dy) % GRID_HEIGHT
            neighbour.append((new_col, new_row))
    return neighbour

def draw_grid(positions):
    for pos in positions:
        col , row = pos
        top_left = (col*TILE_SIZE, row*TILE_SIZE)
        pygame.draw.rect(screen, WHITE, (*top_left, TILE_SIZE, TILE_SIZE))


    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    
def main():
    running = True
    playing = True
    count = 0
    update_freq = 120
    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
            if count > update_freq:
                positions = adjust_positions(positions)
                count = 0
        pygame.display.set_caption(f"Game of Life - FPS: {int(clock.get_fps())}")
        pygame.display.set_caption("playing" if playing else "paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // TILE_SIZE
                row = event.pos[1] // TILE_SIZE
                pos = (col, row)
                if pos in positions:    
                    positions.remove(pos)
                else:
                    positions.add(pos)  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5)*GRID_WIDTH)
                          
        screen.fill(BLACK)
        draw_grid(positions)
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()