import pygame as pg
import sys
# Initialize Pygame
pg.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

font = pg.font.SysFont('times new roman', 20)

class TextInputBox:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def update(self):
        # You can add update logic here if needed
        pass

    def render(self, screen):
        text_surfaceN = font.render(self.text, True, black)
        screen.blit(text_surfaceN, (self.rect.x + 5, self.rect.y + 5))


class PromptInputBox:
    def __init__(self, x, y, width, height, rows, cols):
        self.rect = pg.Rect(x, y, width, height)
        self.prompts = []
        self.rows = rows
        self.cols = cols
    def update(self):
        # You can add update logic here if needed
        pass

    def render(self, screen):
        self.prompts = []
        for i in range(self.rows):
            for j in range(self.cols):
                prompt_text = f"Enter element ({i}, {j}): "
                self.prompts.append(prompt_text)

        for idx, prompt_text in enumerate(self.prompts):
            prompt_surface = font.render(prompt_text, True, black)
            screen.blit(prompt_surface, (self.rect.x + 5, self.rect.y + 5 + idx * 25))
