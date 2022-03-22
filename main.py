import numpy as np
import settings
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("bubble and insertion sort")
CLOCK = pygame.time.Clock()

def displayList(dataset: list, on_index: int) -> None:
    SCREEN.fill('black')
    CLOCK.tick(settings.FPS)
    pygame.event.get()

    percentages = [item/max(dataset) for item in dataset]
    bar_width = round(SCREEN.get_width() / len(percentages))    
    for i, percent in enumerate(percentages):
        x = i * bar_width
        bar = pygame.rect.Rect(x, 0, bar_width, SCREEN.get_height() * percent)
        bar.bottom = SCREEN.get_height()
        pygame.draw.rect(SCREEN, 'red' if i == on_index else 'white', bar)
    pygame.display.update()

def bubbleSort(dataset: list) -> list:
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
    for i, item in enumerate(dataset):
        displayList(dataset, i)
        pos = i
        while pos > 0 and dataset[pos-1] > item:
            dataset[pos] = dataset[pos-1]
            pos -= 1
            displayList(dataset, pos)
        dataset[pos] = item
    return dataset

def main():
    unsorted = np.random.randint(1,100, 100)
    print("bubble sort:", bubbleSort(unsorted))

    unsorted = np.random.randint(1,100, 100)
    print("insertion sort:", insertionSort(unsorted))

    pygame.quit()

if __name__ == "__main__":
    main()