import pygame

from falling_letters.config import cfg_item
from falling_letters.entities.manager import Manager

class App:

    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(cfg_item("game", "screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","caption"))

        pygame.mouse.set_visible(False)

        self.__is_running = False

        self.__clock = pygame.time.Clock()

        self.__manager = Manager()

    def run(self):
        self.__is_running = True

        while self.__is_running:
            delta_time = self.__clock.tick(cfg_item("game", "sync", "fps"))
            self.__handle_input()
            self.__update(delta_time)
            self.__render()

        self.__release()

    def __handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__is_running = False
                self.__manager.handle_input(event)

    def __update(self, delta_time):
        self.__manager.update(delta_time)

    def __render(self):
        self.__screen.fill(cfg_item("game", "bg_color"))
        self.__manager.render(self.__screen)
        pygame.display.update()

    def __release(self):
        pygame.quit()