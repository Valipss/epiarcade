import sys
import os
from enum import Enum
from typing import Any

# Import class
from src.misc import *

# Import non-standard modules
import pygame
from pygame.locals import *
import pygame_menu # https://pygame-menu.readthedocs.io/en/4.2.4/index.html

class View(Enum):
  LOGIN_MENU = 1
  GAMES_LIST_MENU = 2
  IN_GAME_MENU = 3

class Game():
  def __init__(self, name, config):
    self.name = name
    self.executablePath = config['EXECUTABLE_PATH']
    self.language = config['LANGUAGE']
    self.dependencies_script = config['DEPENDENCIES_SCRIPT']
    self.inputs = config['INPUTS']
    self.version = config['VERSION']

class Launcher:
  def __init__(self):
    self.view = View.LOGIN_MENU
    self.selectedGame = None
    self.availableGames = dict()

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

  def launchGame(self, selected: Any, value: int):
    # print(value)
    self.selectedGame = value
    print(self.selectedGame)

  def __initComponents(self):
# LOGIN MENU
    self.loginMenu = pygame_menu.Menu(title = "Login", width = 1080, height = 720, theme = pygame_menu.themes.THEME_DARK)
    loginMenuContent = \
      "Pull your student card out of your wallet\n"\
      "Place the card in front of the reader\n"\
      "Enjoy !\n"
    self.loginMenu.add.label(loginMenuContent, max_char = -1, font_size = 24)

# GAMES LIST MENU
    self.gamesListMenu = pygame_menu.Menu(title = "Games List", width = 1080, height = 720, theme = pygame_menu.themes.THEME_DARK)
    self.gamesListMenu.add.selector(
      title = 'Choose game ',
      items = list(zip(self.availableGames.keys(), self.availableGames.keys())),
      default = 0,
      onreturn = self.launchGame,
    )

  def __loadAvailableGames(self):
    mainFolder = './games'
    gameFolders = [name for name in os.listdir(mainFolder) if os.path.isdir(os.path.join(mainFolder, name))]
    for gameName in gameFolders:
      config = Misc.read_yaml(file_path=mainFolder + "/" + gameName + "/config.yaml")
      self.availableGames[gameName] = Game(name=gameName, config=config)

  def runPyGame(self):
    pygame.init()

    fps = 60.0
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    self.__loadAvailableGames()
    self.__initComponents()

    # Main game loop.
    dt = 1/fps
    while True:
      self.__update(dt)
      self.__draw(screen)
      dt = fpsClock.tick(fps)