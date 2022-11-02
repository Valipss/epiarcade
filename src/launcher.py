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

from src import jadoor
from src.jadoor.credit import Credit
# Import class
from src.misc import Misc

pygame.joystick.init();

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
            executable="./" + self.executablePath,
            capture_output=True,
            cwd="games/" + self.name + "/"
        )
        launcher.view = View.LOGIN_MENU


class Launcher:

    def __init__(self):
        self.view = View.LOGIN_MENU
        self.connectedUsers = [None]
        self.selectedGame = None
        self.availableGames = dict()
        self.logout_timer = 0
        self.jadoor = jadoor.JaDoor()
        self.credit = jadoor.credit.Credit()

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
        elif self.view == View.IN_GAME_MENU:
            self.inGameMenu.update(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__handleKeydown(event)
            elif event.type == QUIT:  # TODO Remove for deployment, we don't want users leaving the launcher
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
        elif self.view == View.IN_GAME_MENU:
            self.inGameMenu.draw(screen)

        pygame.display.flip()

    def __updateSoloScoreboard(self, selected: Any, value: int):
        for i in range(len(self.soloScoreboard._rows) - 1, 0, -1):
            self.soloScoreboard.remove_row(self.soloScoreboard._rows[i])
        scoreboard = selected[0][1].scoreboards['SOLO']
        if scoreboard:
            for i in range(len(scoreboard)):
                topColors = ['gold', 'silver', 'darkorange3']
                self.soloScoreboard.add_row([f'#{i + 1}', scoreboard[i]['username'], scoreboard[i]['score']], cell_font=self.arcadeFont20,
                                            cell_font_color=topColors[i] if i < 3 else 'white')
        else:
            self.soloScoreboard.add_row(['---', "---", "---"], cell_font=self.arcadeFont20, cell_font_color='white')
        self.soloScoreboard.update_cell_style(-1, -1, border_position=pygame_menu.locals.POSITION_NORTH)
        self.soloScoreboard.update_cell_style(-1, 1, font=self.arcadeFont40, border_width=0)

    def __launchSoloGame(self, selected: Any, value: int):
        if self.credit.check(self.connectedUsers[0].login) is False:
            return
        self.selectedGame = selected[0][1]
        self.view = View.IN_GAME_MENU
        t = Thread(target=self.selectedGame.launch, args=("solo", self.connectedUsers, self))
        self.credit.consume(self.connectedUsers[0].login)
        t.start()

    def __launchDuoGame(self, selected: Any, value: int):
        if self.credit.check(self.connectedUsers[0].login) is False or self.credit.check(self.connectedUsers[1].login) is False:
            return
        self.selectedGame = selected[0][1]
        self.view = View.IN_GAME_MENU
        t = Thread(target=self.selectedGame.launch, args=("duo", self.connectedUsers, self))
        self.credit.consume(self.connectedUsers[0].login)
        self.credit.consume(self.connectedUsers[1].login)
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
        self.arcadeFont20 = pygame_menu.font.get_font("medias/ArcadeFont.ttf", 20)
        self.arcadeFont40 = pygame_menu.font.get_font("medias/ArcadeFont.ttf", 40)
        mainTheme = pygame_menu.themes.THEME_DARK.copy()
        mainTheme.set_background_color_opacity(0.6)
        mainTheme.title_font = self.arcadeFont40
        mainTheme.widget_font = self.arcadeFont40

        # LOGIN MENU
        self.loginMenu = pygame_menu.Menu(title="Login", width=1600, height=900, theme=mainTheme)
        loginMenuContent = \
            "Pull your student card out of your wallet\n" \
            "Place the card in front of the reader\n" \
            "Enjoy !\n"
        self.loginMenu.add.label(loginMenuContent, max_char=-1)

        # GAMES LIST MENU
        # SOLO
        self.soloGamesListMenu = pygame_menu.Menu(title="Games List (SOLO)", width=1600, height=900, theme=mainTheme)
        if len(self.__getAvailablesGames(mode='solo')):
            self.soloGamesListMenu.add.label("Student login: None", 'login_message')
            self.soloGamesListMenu.add.label("Credit state unknown", 'credit_message')
            self.soloGamesListMenu.add.label("Logout in ? seconds", 'logout_timer')
            soloGameSelector = self.soloGamesListMenu.add.selector(
                title='Choose a game ',
                items=self.__getAvailablesGames(mode='solo'),
                default=0,
                onchange=self.__updateSoloScoreboard,
                onreturn=self.__launchSoloGame,
            )

            self.soloScoreboard = self.soloGamesListMenu.add.table()
            self.soloScoreboard.translate(0, 40)
            self.soloScoreboard.default_cell_padding = 20
            self.soloScoreboard.add_row(['#RANK', 'Epitech login', "SCORE"], cell_font=self.arcadeFont20, cell_font_color='white')
            scoreboard = soloGameSelector.get_value()[0][1].scoreboards['SOLO']
            if scoreboard:
                for i in range(len(scoreboard)):
                    topColors = ['gold', 'slategray3', 'darkorange3']
                    self.soloScoreboard.add_row([f'#{i + 1}', scoreboard[i]['username'], scoreboard[i]['score']], cell_font=self.arcadeFont20,
                                                cell_font_color=topColors[i] if i < 3 else 'white')
            else:
                self.soloScoreboard.add_row(['---', "---", "---"], cell_font=self.arcadeFont20, cell_font_color='white')
            self.soloScoreboard.update_cell_style(-1, -1, border_position=pygame_menu.locals.POSITION_NORTH)
            self.soloScoreboard.update_cell_style(-1, 1, font=self.arcadeFont40, border_width=0)
        else:
            self.soloGamesListMenu.add.label("No games found", max_char=-1)
            self.soloGamesListMenu.add.label("Student login: None", 'login_message')
            self.soloGamesListMenu.add.label("Credit state unknown", 'credit_message')

        # DUO
        self.duoGamesListMenu = pygame_menu.Menu(title="Games List (DUO)", width=1600, height=900, theme=mainTheme)
        if len(self.__getAvailablesGames(mode='duo')):
            duoGameSelector = self.duoGamesListMenu.add.selector(
                title='Choose a game ',
                items=self.__getAvailablesGames(mode='duo'),
                default=0,
                # onchange = self.__updateDuoScoreboard,
                onreturn=self.__launchDuoGame,
            )

            self.duoScoreboard = self.duoGamesListMenu.add.table()
            self.duoScoreboard.translate(0, 40)
            self.duoScoreboard.default_cell_padding = 20
            self.duoScoreboard.add_row(['#RANK', 'Epitech login', 'SCORE'], cell_font=self.arcadeFont20, cell_font_color='white')
            scoreboard = duoGameSelector.get_value()[0][1].scoreboards['DUO']
            if scoreboard:
                for i in range(len(scoreboard)):
                    topColors = ['gold', 'slategray3', 'darkorange3']
                    self.duoScoreboard.add_row([f'#{i + 1}', scoreboard[i]['username'], scoreboard[i]['score']], cell_font=self.arcadeFont20,
                                               cell_font_color=topColors[i] if i < 3 else 'white')
            else:
                self.duoScoreboard.add_row(['---', "---", "---"], cell_font=self.arcadeFont20, cell_font_color='white')
            self.duoScoreboard.update_cell_style(-1, -1, border_position=pygame_menu.locals.POSITION_NORTH)
            self.duoScoreboard.update_cell_style(-1, 1, font=self.arcadeFont40, border_width=0)
        else:
            self.duoGamesListMenu.add.label("No games found", max_char=-1)
        
        #IN GAME MENU
        self.inGameMenu = pygame_menu.Menu(title="", width=1600, height=900, theme=mainTheme)
        self.inGameMenu.add.label("Game is still running", max_char=-1)


    def __loadAvailableGames(self):
        mainFolder = './games'
        gameFolders = [name for name in os.listdir(mainFolder) if os.path.isdir(os.path.join(mainFolder, name))]
        for gameName in gameFolders:
            config = Misc.read_yaml(file_path=mainFolder + "/" + gameName + "/config.yaml")
            self.availableGames[gameName] = Game(name=gameName, config=config)

    def runPyGame(self):
        pygame.init()

        fps = 60
        fpsClock = pygame.time.Clock()
        screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

        self.__loadAvailableGames()
        self.__initComponents()

        # Main game loop.
        dt = 1 / fps
        student_login = None
        while True:
            self.__update(dt)
            self.__draw(screen)
            if self.view == View.LOGIN_MENU:
                if student_login is None:
                    student_login = self.jadoor.read()
                else:
                    self.connectedUsers[0] = User(student_login)
                    student_login = None
                    self.view = View.SOLO_GAMES_LIST_MENU
                    self.soloGamesListMenu.get_widget('login_message').set_title("Login: " + self.connectedUsers[0].login)
                    self.soloGamesListMenu.get_widget('credit_message').set_title("Credits: " + str(int(self.credit.check(self.connectedUsers[0].login))))
                    self.logout_timer = 1800
                    self.soloGamesListMenu.get_widget('logout_timer').set_title("Logout in " + str(int(self.logout_timer / 60)) + " seconds")
            elif self.view in [View.SOLO_GAMES_LIST_MENU, View.DUO_GAMES_LIST_MENU]:
                self.soloGamesListMenu.get_widget('logout_timer').set_title("Logout in " + str(int(self.logout_timer / 60)) + " seconds")
                self.logout_timer -= 1
                if self.logout_timer == 0:
                    self.view = View.LOGIN_MENU
                    self.connectedUsers = [None]
            dt = fpsClock.tick(fps)
