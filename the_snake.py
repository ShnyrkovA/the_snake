from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject используется для создания сущностей."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = list(position)
        self.body_color = body_color

    def draw(self):
        """Переопределяется в дочерних классах для отрисовки объекта."""
        pass


class Snake(GameObject):
    """Класс Snake используется для создания сущности змейки."""

    def __init__(self):
        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
        )
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Задает направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Определяет логику перемещения змейки и её взаимодействие с полем."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)
        new_head = (
            new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT
        )

        if new_head in self.positions[1:]:
            self.reset()
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position[0], position[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.positions[0][0], self.positions[0][1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                self.last[0], self.last[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


class Apple(GameObject):
    """Класс Apple используется для создания сущности яблока."""

    def __init__(self, position=None):
        if position is None:
            position = self.randomize_position()
        super().__init__(position, body_color=APPLE_COLOR)

    def randomize_position(self):
        """Генерирует случайную начальную позицию яблока на сетке."""
        return [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        ]

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Функция управления змейкой с помощью клавиш стрелок."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == tuple(apple.position):
            snake.length += 1
            apple = Apple()
            snake.draw()
            apple.draw()
            pygame.display.update()

        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана перед отрисовкой

        if snake.positions != apple.position:
            snake.draw()
            apple.draw()
            pygame.display.update()


if name == '__main__':
    main()
