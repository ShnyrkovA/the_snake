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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """Класс GameObject(Родительский) используется для создания сущностей,
    змейки, яблока и т.д.
    """

    def __init__(self, position=(0, 0), body_color=None):
        self.position = list(position)
        self.body_color = body_color

    def draw(self):
        """Описывает работу функции draw
        (переопределяется в других классах).
        """
        pass


class Snake(GameObject):
    """Класс Snake(Дочерний) используется для создания сущности змейки."""

    def __init__(self):
        # Инициализация позиции и цвета через родительский класс GameObject
        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
        )

        self.positions = [self.position[:]]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Описывает работу функции update_direction
        направление змейки задает.
        """
        if self.next_direction:
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Данная функция описывает саму физику движения змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(
            self.positions[0][0], self.positions[0][1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.last[0], self.last[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку до начальных параметров."""
        self.length = 1  # Сброс длины
        self.positions = [(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


class Apple(GameObject):
    
    """Класс Apple используется для создания сущности яблока."""

    def __init__(self):
        super().__init__()
        self.position = self.random_position()
        self.body_color = APPLE_COLOR

    def random_position(self):
        """Генерирует случайную позицию для яблока."""
        return [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        ]

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    pygame.init()

    snake = Snake()
    apple = Apple()

    running = True

    while running:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.next_direction = RIGHT

        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.random_position()

        # Обновление экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
