import os
import subprocess
import sys
from enum import Enum
from threading import Thread
from typing import Any

# Import non-standard modules
import pygame
import pygame_menu  # https://pygame-menu.readthedocs.io/en/4.2.4/index.html
from pygame.locals import *

# Import class
from src.misc import Misc
from src import jadoor


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
    self.scoreboards = Misc.read_yaml(file_path="games/" + self.name + "/scoreboard.yaml")
  
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
        self.connectedUsers = [None]  # TODO set as None for deployment
        self.selectedGame = None
        self.availableGames = dict()
        self.jadoor = jadoor.JaDoor()

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
            elif event.type == QUIT:  # TODO Remove for deployment, we don't want users leaving the launcher
                pygame.quit()
                sys.exit()

    def __draw(self, screen):
        screen.fill((0, 0, 0))

        self.menuBackground.draw(screen)
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
        return list(zip(ret.keys(), ret.values()))

    def __initComponents(self):  
  # SHARED CONTENT
      self.menuBackground = pygame_menu.BaseImage(image_path="medias/arcade_bg.jpg")
      arcadeFont20 = pygame_menu.font.get_font("medias/ArcadeFont.ttf", 20)
      arcadeFont40 = pygame_menu.font.get_font("medias/ArcadeFont.ttf", 40)
      mainTheme = pygame_menu.themes.THEME_DARK.copy()
      mainTheme.set_background_color_opacity(0.6)
      mainTheme.title_font = arcadeFont40
      mainTheme.widget_font = arcadeFont40


  # LOGIN MENU
      self.loginMenu = pygame_menu.Menu(title = "Login", width = 1600, height = 900, theme = mainTheme)
      loginMenuContent = \
        "Pull your student card out of your wallet\n"\
        "Place the card in front of the reader\n"\
        "Enjoy !\n"
      self.loginMenu.add.label(loginMenuContent, max_char = -1)

  # GAMES LIST MENU
    # SOLO
      self.soloGamesListMenu = pygame_menu.Menu(title = "Games List (SOLO)", width = 1600, height = 900, theme = mainTheme)
      if len(self.__getAvailablesGames(mode='solo')):
        soloGameSelector = self.soloGamesListMenu.add.selector(
          title = 'Choose a game ',
          items = self.__getAvailablesGames(mode='solo'),
          default = 0,
          # onchange = self.__updateSoloScoreboard,
          onreturn = self.__launchSoloGame,
        )

        self.soloScoreboard = self.soloGamesListMenu.add.table()
        self.soloScoreboard.translate(0, 40)
        self.soloScoreboard.default_cell_padding = 20
        self.soloScoreboard.add_row(['#RANK', 'Epitech login', "SCORE"], cell_font=arcadeFont20, cell_font_color='white')
        scoreboard = soloGameSelector.get_value()[0][1].scoreboards['SOLO']
        for i in range(len(scoreboard)):
          topColors = ['gold', 'silver', 'darkorange3']
          self.soloScoreboard.add_row([f'#{i + 1}', scoreboard[i]['username'], scoreboard[i]['score']], cell_font=arcadeFont20,
                          cell_font_color=topColors[i] if i < 3 else 'white')
        self.soloScoreboard.update_cell_style(-1, -1, border_position=pygame_menu.locals.POSITION_NORTH)
        self.soloScoreboard.update_cell_style(-1, 1, font=arcadeFont40, border_width=0)
      else:
        self.soloGamesListMenu.add.label("No games found", max_char=-1, font=arcadeFont40)

    # DUO
      self.duoGamesListMenu = pygame_menu.Menu(title = "Games List (DUO)", width = 1600, height = 900, theme = mainTheme)
      if len(self.__getAvailablesGames(mode='duo')):
        duoGameSelector = self.duoGamesListMenu.add.selector(
          title = 'Choose a game ',
          items = self.__getAvailablesGames(mode='duo'),
          default = 0,
          # onchange = self.__updateDuoScoreboard,
          onreturn = self.__launchDuoGame,
        )

        self.duoScoreboard = self.duoGamesListMenu.add.table()
        self.duoScoreboard.translate(0, 40)
        self.duoScoreboard.default_cell_padding = 20
        self.duoScoreboard.add_row(['#RANK', 'Epitech login', 'SCORE'], cell_font=arcadeFont20, cell_font_color='white')
        scoreboard = duoScoreboard.get_value()[0][1].scoreboards['DUO']
        for i in range(len(scoreboard)):
          topColors = ['gold', 'silver', 'brown4']
          self.duoScoreboard.add_row([f'#{i + 1}', scroreboard[i]['username'], scroreboard[i]['score']], cell_font=arcadeFont20,
                          cell_font_color=topColors[i] if i < 3 else 'white')
        self.duoScoreboard.update_cell_style(-1, -1, border_position=pygame_menu.locals.POSITION_NORTH)
        self.duoScoreboard.update_cell_style(-1, 1, font=arcadeFont40, border_width=0)
      else:
        self.duoGamesListMenu.add.label("No games found", max_char = -1)

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
        dt = 1 / fps
        while True:
            self.__update(dt)
            self.__draw(screen)
            if self.view == View.LOGIN_MENU:
                student_login = self.jadoor.read()
                if student_login:
                    self.connectedUsers[0] = User(student_login)
                    self.view = View.SOLO_GAMES_LIST_MENU
            dt = fpsClock.tick(fps)
