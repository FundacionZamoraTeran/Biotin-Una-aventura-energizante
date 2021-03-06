import sys
import os
import pygame

from gi.repository import Gtk
from scenarios.utils import utils, consts, saves
from scenarios.menu.button import Button
from scenarios.menu.save_state import SaveState

class Start:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.background = utils.load_image("start_door/background.png", "menu")
        self.title = utils.load_image("start_door/title.png", "menu")
        self.save = saves.load()

        self.slot1 = SaveState((225, 330),
                               (280, 315),
                               (600, 340),
                               ("slot1.png", "slot2.png"),
                               "menu/start_door",
                               self.save["slot_1"],
                               flag=True)

        self.slot2 = SaveState((225, 480),
                               (280, 465),
                               (600, 490),
                               ("slot1.png", "slot2.png"),
                               "menu/start_door",
                               self.save["slot_2"],
                               flag=False)

        self.slot3 = SaveState((225, 630),
                               (280, 615),
                               (600, 640),
                               ("slot1.png", "slot2.png"),
                               "menu/start_door",
                               self.save["slot_3"],
                               flag=False)

        self.exit_button = Button(1030,
                                  120,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  36,
                                  38)
        self.level_selected = None
        self.slot_selected =None

    def run(self):
        """
            control the actions happening on the start modal
            you can start from any save but it will eventually overwrite
            a previous save slot.
        """
        running = True
        while running:
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        running = False
                    elif event.key == pygame.K_RETURN or event.key == consts.K_CHECK:
                        if self.slot1.flag is True:
                            self.level_selected = 0
                            self.slot_selected = "slot_1"
                        elif self.slot2.flag is True:
                            self.level_selected = 0
                            self.slot_selected = "slot_2"
                        elif self.slot3.flag is True:
                            self.level_selected = 0
                            self.slot_selected = "slot_3"
                        running = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.slot1.flag is True:
                            self.slot1.flag = False
                            self.slot2.flag = True
                        elif self.slot2.flag is True:
                            self.slot2.flag = False
                            self.slot3.flag = True

                    elif event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        if self.slot2.flag is True:
                            self.slot2.flag = False
                            self.slot1.flag = True
                        elif self.slot3.flag is True:
                            self.slot3.flag = False
                            self.slot2.flag = True

            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (255, 190))
            self.slot1.render(self.screen2)
            self.slot2.render(self.screen2)
            self.slot3.render(self.screen2)
            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
