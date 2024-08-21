import pygame
from typing import List, Optional
from searches import node_to_path, astar

# Pygame settings
TILE_SIZE = 100
MARGIN = 5
SCREEN_SIZE = (TILE_SIZE * 3 + MARGIN * 4, TILE_SIZE * 3 + MARGIN * 4)
BACKGROUND_COLOR = (30, 30, 30)
TILE_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
FPS = 2


def main():
    seq: List[str] = [" ", "1", "2", "3", "4", "5", "6", "7", "8"]
    start: Puzzle_state = Puzzle_state(seq)
    print("Finding a soltution...\n")
    solution: Optional[Puzzle_state] = astar(
        start, goal_test, Puzzle_state.get_sucessors, get_manhattan_distance
    )
    if solution is None:
        print("No solution found")
    else:
        path: List[Puzzle_state] = node_to_path(solution)
        visualize_solution(path)


class Puzzle_state:

    def __init__(self, sequence: List[str]) -> None:
        self.sequence = sequence

    def __str__(self) -> str:
        sequence = self.sequence
        a = ""
        for i in range(len(sequence)):
            a = a + sequence[i] + "\t"
            if (i + 1) % 3 == 0:
                a = a + "\n"
        return a

    def get_sucessors(self) -> List:
        sucssores: List[Puzzle_state] = []
        sequence = self.sequence
        i = sequence.index(" ")

        moves = [-1, 1, -3, 3]

        for m in moves:
            if 0 <= i + m < 9:
                if i % 3 == 0 and m == -1:
                    continue
                if i % 3 == 2 and m == 1:
                    continue
                new_sequence = swap_indexes(sequence, i, i + m)
                sucssores.append(Puzzle_state(new_sequence))

        return sucssores


def get_manhattan_distance(state: Puzzle_state) -> int:
    distance = 0
    for tile in range(1, 9):
        current_index = state.sequence.index(str(tile))
        target_index = tile - 1
        dx = abs(current_index % 3 - target_index % 3)
        dy = abs(current_index // 3 - target_index // 3)
        distance = distance + dx + dy
    return distance


def goal_test(state: Puzzle_state) -> bool:
    return state.sequence == ["1", "2", "3", "4", "5", "6", "7", "8", " "]


def swap_indexes(lst: List[str], index1: int, index2: int) -> List[str]:
    new_lst = lst.copy()
    new_lst[index1], new_lst[index2] = new_lst[index2], new_lst[index1]
    return new_lst


def visualize_solution(path: List[Puzzle_state]) -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("8-Puzzle Solver")
    clock = pygame.time.Clock()

    for state in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BACKGROUND_COLOR)
        draw_state(screen, state)
        pygame.display.flip()
        clock.tick(FPS)

    # Wait for a key press to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()


def draw_state(screen, state: Puzzle_state):
    for i, tile in enumerate(state.sequence):
        if tile != " ":
            x = (i % 3) * (TILE_SIZE + MARGIN) + MARGIN
            y = (i // 3) * (TILE_SIZE + MARGIN) + MARGIN
            pygame.draw.rect(
                screen, TILE_COLOR, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            )
            draw_text(screen, tile, x, y)


def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 72)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
    screen.blit(text_surf, text_rect)


if __name__ == "__main__":
    main()
