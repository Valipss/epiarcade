import sys
import os
import subprocess
from threading import Thread
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
  SOLO_GAMES_LIST_MENU = 2
  DUO_GAMES_LIST_MENU = 3
  IN_GAME_MENU = 4

class User():
  def __init__(self, login):
    self.login = login


class Game():
  def __init__(self, name, config):
    self.name = name
    self.executablePath = config['EXECUTABLE_PATH']
    self.language = config['LANGUAGE']
    self.dependencies_script = config['DEPENDENCIES_SCRIPT']
    self.inputs = config['INPUTS']
    self.version = config['VERSION']
    self.modes = config['GAMEMODES']
  
  def launch(self, mode, users, launcher):
    u = [user.login for user in users]
    process = subprocess.run(
      args=[mode, ''.join(u)],
      executable="games/" + self.name + "/" + self.executablePath,
      capture_output=True
    )
    if process.returncode == 42:
      launcher.view = View.LOGIN_MENU

class Launcher:
  def __init__(self):
    self.view = View.LOGIN_MENU
    self.connectedUsers = [User("hubert.bonisseur-de-la-bath@epitech.eu")] # TODO set as None for deployment
    self.selectedGame = None
    self.availableGames = dict()

  def __handleKeydown(self, event):
    if event.unicode == 's':
      self.view = View.SOLO_GAMES_LIST_MENU
    elif event.unicode == 'd':
      self.view = View.DUO_GAMES_LIST_MENU

  def __update(self, dt):
    events = pygame.event.get()

    currentView = self.view
    if self.view == View.LOGIN_MENU:
      self.loginMenu.update(events)
    elif self.view == View.SOLO_GAMES_LIST_MENU:
      self.soloGamesListMenu.update(events)
    elif self.view == View.DUO_GAMES_LIST_MENU:
      self.duoGamesListMenu.update(events)

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
    elif self.view == View.SOLO_GAMES_LIST_MENU:
      self.soloGamesListMenu.draw(screen)
    elif self.view == View.DUO_GAMES_LIST_MENU:
      self.duoGamesListMenu.draw(screen)

    pygame.display.flip()

  def __launchSoloGame(self, selected: Any, value: int):
    self.selectedGame = self.availableGames[value]
    self.view = View.IN_GAME_MENU
    t = Thread(target=self.selectedGame.launch, args=("solo", self.connectedUsers, self))
    t.start()

  def __launchDuoGame(self, selected: Any, value: int):
    self.selectedGame = self.availableGames[value]
    self.view = View.IN_GAME_MENU
    t = Thread(target=self.selectedGame.launch, args=("duo", self.connectedUsers, self))
    t.start()

  def __getAvailablesGames(self, mode):
    ret = dict()
    for game in self.availableGames.values():
      if mode in game.modes:
        ret[game.name] = self.availableGames[game.name]
    return list(zip(ret.keys(), ret.keys()))

  def __initComponents(self):
# LOGIN MENU
    self.loginMenu = pygame_menu.Menu(title = "Login", width = 1080, height = 720, theme = pygame_menu.themes.THEME_DARK)
    loginMenuContent = \
      "Pull your student card out of your wallet\n"\
      "Place the card in front of the reader\n"\
      "Enjoy !\n"
    self.loginMenu.add.label(loginMenuContent, max_char = -1, font_size = 24)

# GAMES LIST MENU
  # SCOREBOARD
    # self.scoreboardTable = pygame_menu.widgets.Table('scoreboard').configured = True
    # self.scoreboardTable.add_row(["test", "test"])

  # SOLO
    self.soloGamesListMenu = pygame_menu.Menu(title = "Games List (SOLO)", width = 1080, height = 720, theme = pygame_menu.themes.THEME_DARK)
    if len(self.__getAvailablesGames(mode='solo')):
      self.soloGamesListMenu.add.selector(
        title = 'Choose a game ',
        items = self.__getAvailablesGames(mode='solo'),
        default = 0,
        # onchange = self.__updateScoreboard(mode='solo'),
        onreturn = self.__launchSoloGame,
      )
    else:
      self.soloGamesListMenu.add.label("No games found", max_char = -1, font_size = 24)

  # DUO
    self.duoGamesListMenu = pygame_menu.Menu(title = "Games List (DUO)", width = 1080, height = 720, theme = pygame_menu.themes.THEME_DARK)
    if len(self.__getAvailablesGames(mode='duo')):
      self.duoGamesListMenu.add.selector(
        title = 'Choose a game ',
        items = self.__getAvailablesGames(mode='duo'),
        default = 0,
        onchange = self.__updateScoreboard,
        onreturn = self.__launchDuoGame,
      )
    else:
      self.duoGamesListMenu.add.label("No games found", max_char = -1, font_size = 24)

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