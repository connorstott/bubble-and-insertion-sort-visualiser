import numpy as np
import settings
import random
import pygame
import time
import sys

pygame.init()
SCREEN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("bubble and insertion sort")
CLOCK = pygame.time.Clock()

class Button:
    button_colour = '#cc6fd6'
    button_hover_colour = '#e4a2eb'
    button_border_colour = '#cf259c'
    button_text_colour = 'white'
    button_font = pygame.font.Font(None, 40)

    unsorted = []

    def __init__(self, width: int, height: int, screen_center_offset: tuple, text: str, action):
        self.screen_center_offset = pygame.math.Vector2(screen_center_offset)
        self.rect = pygame.Rect((0,0), (width, height))
        self.text = self.button_font.render(text, True, self.button_text_colour)
        self.text_rect = self.text.get_rect(center = self.rect.center)

        self.action = action
    
    def draw(self) -> None:
        """draws button to screen"""
        border = self.rect.inflate(10, 10)
        pygame.draw.rect(SCREEN, self.button_border_colour, border, border_radius=10)
        pygame.draw.rect(SCREEN, self.colour, self.rect, border_radius=10)
        SCREEN.blit(self.text, self.text_rect)
    
    def update(self) -> None:
        """called once per frame"""
        self.rect.centerx = SCREEN.get_width()//2 + self.screen_center_offset.x
        self.rect.centery = SCREEN.get_height()//2 + self.screen_center_offset.y
        self.text_rect.center = self.rect.center

        self.checkHover()
        self.draw()
        self.checkClicked()
    
    def checkHover(self) -> None:
        """checks for mouse hover over button"""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_x, mouse_y):
            self.colour = self.button_hover_colour
        else:
            self.colour = self.button_colour
    
    def checkClicked(self) -> None:
        """action for when button pressed"""
        mouses_pressed = pygame.mouse.get_pressed()
        if not mouses_pressed[0]: return False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.action(self.unsorted)
            time.sleep(0.5)

def displayList(dataset: list, on_index: int, update: bool = True) -> None:
    """puts the list onto the pygame screen"""
    SCREEN.fill('black')
    CLOCK.tick(settings.FPS)
    pygame.event.get()

    max_bar = max(dataset)
    percentages = [item/max_bar for item in dataset]
    bar_width = round(SCREEN.get_width() / len(percentages))    
    for i, percent in enumerate(percentages):
        x = i * bar_width
        bar = pygame.rect.Rect(x, 0, bar_width, SCREEN.get_height() * percent)
        bar.bottom = SCREEN.get_height()
        pygame.draw.rect(SCREEN, 'red' if i == on_index else 'white', bar)
    
    if update: pygame.display.update()

def bubbleSort(dataset: list) -> list:
    """bubble sorts a given dataset"""
    dataset = dataset.copy()
    sorted = False
    while not sorted:
        sorted = True
        for i, item in enumerate(dataset):
            displayList(dataset, i)
            if i == len(dataset) - 1:
                break
            if dataset[i] <= dataset[i+1]:
                continue
            sorted = False
            dataset[i] = dataset[i+1]
            dataset[i+1] = item
    return dataset

def insertionSort(dataset: list) -> list:
    """insertion sorts a given dataset"""
    dataset = dataset.copy()
    for i, item in enumerate(dataset):
        displayList(dataset, i)
        pos = i
        while pos > 0 and dataset[pos-1] > item:
            dataset[pos] = dataset[pos-1]
            pos -= 1
            dataset[pos] = item
            displayList(dataset, pos)
    return dataset

def newUnsorted(*kwargs) -> list:
    """gets a new unsorted and gives it to the Button class"""
    unsorted = [i for i in range(1,101)]
    random.shuffle(unsorted)
    Button.unsorted = unsorted

def menu() -> None:
    newUnsorted()

    bubble_button = Button(300, 100, (- 175, 0), "bubble sort", bubbleSort)
    inserton_button = Button(300, 100, (175, 0), "insertion sort", insertionSort)
    new_unsorted = Button(150, 50, (0, 110), "new array", newUnsorted)
    buttons = [bubble_button, inserton_button, new_unsorted]

    while True:
        CLOCK.tick(settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #return

        displayList(Button.unsorted, 0, update=False)

        for button in buttons: button.update()

        pygame.display.update()

def main():
    menu()

    # import cProfile
    # import pstats
    # with cProfile.Profile() as pr:
    #     menu()
    
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

if __name__ == "__main__":
    main()
