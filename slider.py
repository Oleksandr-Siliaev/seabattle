import pygame
from drawing import screen


class Slider:
    def __init__(
            self,
            x_offset: int,
            y_offset: int,
            width: int,
            height: int,
            color: tuple,
            handle_color: tuple,
            value: float) -> None:
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.color = color
        self.handle_color = handle_color
        self.value = value  # Значение громкости (от 0 до 1)
        self.dragging = False
        self.rect = pygame.Rect(
            self.x_offset,
            self.y_offset,
            self.width,
            self.height)
        self.font = pygame.font.Font(None, 20)
        # Ползунок
        self.handle_width = 10  # Ширина ползунка
        # Высота ползунка (увеличена для визуального эффекта)
        self.handle_height = self.height + 4
        self.handle_rect = pygame.Rect(
            self.x_offset + int(self.value * self.width)
            - self.handle_width // 2,
            self.y_offset - 2,
            self.handle_width,
            self.handle_height,
        )

    def draw(self):
        # Отрисовка полоски ползунка
        pygame.draw.rect(screen, self.color, self.rect)

        # Отрисовка ползунка
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)

        volume_text = f"Volume: {int(self.value * 100)}%"
        text_surface = self.font.render(volume_text, True, self.handle_color)
        text_rect = text_surface.get_rect(
            center=(
                self.x_offset +
                self.width //
                2,
                self.y_offset -
                30))
        screen.blit(text_surface, text_rect)

    def update_value(self, mouse_x):
        # Обновление значения ползунка на основе позиции мыши
        relative_x = mouse_x - self.x_offset
        self.value = max(0, min(1, relative_x / self.width)
                         )  # Значение ограничено от 0 до 1

        # Обновление положения ползунка
        self.handle_rect.x = self.x_offset + \
            int(self.value * self.width) - self.handle_width // 2

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.handle_rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False

    def move(self, mouse_x):
        # Ограничиваем позицию ползунка в пределах прямоугольника полоски
        mouse_x = max(self.x_offset, min(mouse_x, self.x_offset + self.width))
        # Обновляем значение ползунка на основе позиции мыши
        relative_x = mouse_x - self.x_offset
        self.value = max(0, min(1, relative_x / self.width)
                         )  # Значение ограничено от 0 до 1
        # Обновляем положение ползунка
        self.handle_rect.x = self.x_offset + \
            int(self.value * self.width) - self.handle_width // 2
