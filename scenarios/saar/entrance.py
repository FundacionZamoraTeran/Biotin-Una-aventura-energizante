import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.saar import hena
from scenarios.saar import hcesar
from scenarios.saar import middle
from actors.player import Player
from actors.enemy import Enemy
from actors.platform import Platform
from actors.prompt import Prompt


class Entrance:
    """
        Class representing the first stage of Saar village, recieves
        a Surface as a screen, and a Clock as clock, and a save slot name
    """
    def __init__(self, screen, clock, slot):
        self.screen = screen
        self.clock = clock
        self.slotname = slot
        self.slot = saves.load_slot(slot)
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.next_level = 1
        self.character = "ena" if self.slot["team_ena"] is True else "diego"
        self.background = utils.load_image("background.png", "saar/stage_1")
        self.background_width = self.background.get_size()[0]
        self.foreground = utils.load_image("foreground.png", "saar/stage_1")
        self.modal = utils.load_image("modal.png", "saar")
        self.ground = Platform(self.screen,
                               self.clock,
                               (0, 742),
                               "ground.png",
                               "saar/stage_1")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (635, 480),
                               "interact.png",
                               "saar",
                               (400, 600))

        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (2155, 480),
                                 "interact.png",
                                 "saar",
                                 (400, 600))
        self.interact_3 = Prompt(self.screen,
                                 self.clock,
                                 (2280, 480),
                                 "interact.png",
                                 "saar",
                                 (400, 600))

        self.player = Player(self.screen,
                             self.clock,
                             (150, 640),
                             self.character,
                             2400,
                             True,
                             collisionable=True)
        self.gali = Enemy(self.screen,
                          self.clock,
                          (1000, 640),
                          "monsters/gali",
                          (300, 1000),
                          16)
        self.menti = Enemy(self.screen,
                           self.clock,
                           (1000, 640),
                           "monsters/menti",
                           (500, 1200),
                           26)
        self.arequi = Enemy(self.screen,
                           self.clock,
                           (1000, 640),
                           "monsters/arequi",
                           (300, 1200),
                           10)
        self.lopop = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/lopop",
                           (1300, 1940),
                           10,
                           35)
        self.vlopop = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/vlopop",
                           (1200, 1640),
                           18,
                           35)
        self.glopop = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/glopop",
                           (1100, 2040),
                           30,
                           35)
        #collision lists
        self.platforms_list = pygame.sprite.Group()
        self.enemies_list = pygame.sprite.Group()
        self.platforms_list.add(self.ground)
        self.help = Button((1058, 39), "h1.png", "h2.png", 82, 82, "saar")
        self.show_help = False
        self.visited = [False, False]

    def run(self):
        utils.load_bg("nocturne.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.screen.blit(self.ground.image, (rel_x, 742))
                self.actors_load(abs(rel_x))
                self.screen.blit(self.foreground, (rel_x, 585))
                if self.show_help:
                    self.screen.blit(self.help.end, (1058, 39))
                    self.screen.blit(self.modal, (0, 0))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.screen.blit(self.ground.image, (rel_x - self.background_width, 742))
                self.actors_load(rel_x)
                self.screen.blit(self.foreground, (rel_x - self.background_width, 585))
                if self.show_help:
                    self.screen.blit(self.help.end, (1058, 39))
                    self.screen.blit(self.modal, (0, 0))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "left"
                        self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "right"
                        self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 620
                                and self.player.real_x+self.player.rect.width < 745):
                            utils.loading_screen(self.screen)
                            hus = hena.Hena(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            self.visited[0] = True
                            utils.load_bg("nocturne.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2140 and
                              self.player.real_x+self.player.rect.width < 2280):
                            utils.loading_screen(self.screen)
                            hus = hcesar.Hcesar(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            self.visited[1] = True
                            utils.load_bg("nocturne.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2280
                              and self.player.real_x+self.player.rect.width < 2401 and
                              all(i is True for i in self.visited)):
                            utils.loading_screen(self.screen)
                            mid = middle.Middle(self.screen, self.clock, self.character)
                            mid.run()
                            del mid
                            running = False
                            utils.loading_screen(self.screen)
                            #save here
                            if not self.slot["stages"]["aldea_1"] is True:
                                saves.save(self.slotname, 2, "Aldea Saar", "aldea_1")
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        self.player.jumping = True
                    elif event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        self.help.on_press(self.screen)
                        if self.show_help is False:
                            self.show_help = True
                        elif self.show_help:
                            self.show_help = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def actors_load(self, rel_x):
        if self.player.real_x < 1500 and not self.gali.defeated:
            if not self.gali.alive():
                self.gali.add(self.enemies_list)
            self.gali.roam(rel_x)
        else:
            if self.gali.alive():
                self.gali.remove(self.enemies_list)
        if self.player.real_x < 1500 and not self.menti.defeated:
            if not self.menti.alive():
                self.menti.add(self.enemies_list)
            self.menti.roam(rel_x)
        else:
            if self.menti.alive():
                self.menti.remove(self.enemies_list)
        if self.player.real_x < 1500 and not self.arequi.defeated:
            if not self.arequi.alive():
                self.arequi.add(self.enemies_list)
            self.arequi.roam(rel_x)
        else:
            if self.arequi.alive():
                self.arequi.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.lopop.defeated:
            if not self.lopop.alive():
                self.lopop.add(self.enemies_list)
            self.lopop.roam(rel_x)
        else:
            if self.lopop.alive():
                self.lopop.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.vlopop.defeated:
            if not self.vlopop.alive():
                self.vlopop.add(self.enemies_list)
            self.vlopop.roam(rel_x)
        else:
            if self.vlopop.alive():
                self.vlopop.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.glopop.defeated:
            if not self.glopop.alive():
                self.glopop.add(self.enemies_list)
            self.glopop.roam(rel_x)
        else:
            if self.glopop.alive():
                self.glopop.remove(self.enemies_list)
        if (self.player.real_x+self.player.rect.width > 620
                and self.player.real_x+self.player.rect.width < 745):
            self.interact.float(rel_x)
        if (self.player.real_x+self.player.rect.width > 2140
                and self.player.real_x+self.player.rect.width < 2280):
            self.interact_2.float(1200)
        if (self.player.real_x+self.player.rect.width > 2280
                and self.player.real_x+self.player.rect.width < 2401 and
                all(i is True for i in self.visited)):
            self.interact_3.float(1200)
        self.player.set_sprite_groups(self.platforms_list, self.enemies_list)
        self.player.update()
