# Import standard modules.
import sys
from enum import Enum
 
# Import non-standard modules.
import pygame
from pygame.locals import *
import pygame_menu # https://pygame-menu.readthedocs.io/en/4.2.4/index.html


class View(Enum):
  LOGIN_MENU = 1
  GAMES_LIST_MENU = 2
  IN_GAME_MENU = 3
  

class Launcher:
  def __init__(self):
    self.view = View.LOGIN_MENU

  def __handleKeydown(self, event):
    if event.unicode == 'n':
      self.view = View.GAMES_LIST_MENU

  def __update(self, dt):
    events = pygame.event.get()

    currentView = self.view
    if self.view == View.LOGIN_MENU:
      self.loginMenu.update(events)
    elif self.view == View.GAMES_LIST_MENU:
      self.gamesListMenu.update(events)

    for event in events:
      if event.type == pygame.KEYDOWN:
        self.__handleKeydown(event)
      elif event.type == QUIT: # TODO Remove for deployment, we don't want users leaving the launcher
        pygame.quit()
        sys.exit()

  def __draw(self, screen):
    screen.fill((0, 0, 0))

    # Redraw screen here.
    currentView = self.view
    if self.view == View.LOGIN_MENU:
      self.loginMenu.draw(screen)
    elif self.view == View.GAMES_LIST_MENU:
      self.gamesListMenu.draw(screen)

    pygame.display.flip()
  
  def __initComponents(self):
    self.loginMenu = pygame_menu.Menu(
      title = "Login",
      width = 1080,
      height = 720,
      theme = pygame_menu.themes.THEME_DARK
    )
    loginMenuContent = \
      "Pull your student card out of your wallet\n"\
      "Place the card in front of the reader\n"\
      "Enjoy !\n"
    self.loginMenu.add.label(loginMenuContent, max_char=-1, font_size=24)

    self.gamesListMenu = pygame_menu.Menu(
      title = "Games List",
      width = 1080,
      height = 720,
      theme = pygame_menu.themes.THEME_DARK
    )
    self.gamesListMenu.add.selector("Select ", ["test"])

  def runPyGame(self):
    pygame.init()

    fps = 60.0
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    self.__initComponents()

    # Main game loop.
    dt = 1/fps
    while True:
      self.__update(dt)
      self.__draw(screen)
      dt = fpsClock.tick(fps)


def main() -> int:
  launcher = Launcher()
  launcher.runPyGame()

if __name__ == '__main__':
    main()