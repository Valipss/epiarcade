---
module:         B-INN-000
title:          EPIARCADE
subtitle:       Créer un jeu sur l'arcade
author:         valentin2.masson@epitech.eu 
version:        1.0
noCleanRepo:     true
noBonusDir:     true
noErrorMess:    true
---

# <u>Requirements</u> #
## Allowed programming languages / Graphical libraries ##
everything that is installable on the last stable version of **Debian**.

## Arcade machine specs / devices ##
- *CPU Intel **J4125** 2.7 GHz with Intel Graphics 600*
- *RAM **8Go** of LPDDR4*
- *Screen size of **1680 x 1050** (16:10) @60Hz*
- *2 joysticks / 12 buttons*


# <u>What is it ?</u> #
The epiarcade is a way for Epitech students to create and "publish" their own games, so others students can play it. Once a day, every student earn a credit (not ECTS :D) to play on the arcade. Just have to pull out your student card and BEEP it !


# <u>Rules</u> #
- Your game must be a **scoring game** => the player(s) should have the desire to play again to improve its score.
- You must code a **SOLO** or **DUO** game (or both).
- Your game **must not** contains any menu or settings.
- The gamemode ("solo" / "duo") has to be chosen with the 1<sup>st</sup> argument sent at the launch to the program. (ex: `./my_epiarcade_game SOLO`)
- The player must enter the game directly at the start of program.
- The program must exit at the end of the game, we encourage you to code an "end screen" displayed during a few seconds before exiting the program.
- The score must be printed in the standard output when the program stops.  
*standard output content (respect this format):*
```bash
    epiarcade:[{"login":"player1@epitech.eu", "score":"42"}, {"login":"player2@epitech.eu", "score":"84"}]
```

# <u>Delivery</u> #
Create a repository and name it as your game title, then create two files `config.yaml` and `scoreboard.yaml`.  

<u>*config.yaml content (copy/paste and **fill**):*</u>
```yaml
EXECUTABLE_PATH: "" # EXAMPLE : 'pacman' or 'bin/pacman'
LANGUAGE: "" # C, C++, python, C# ...
VERSION: "" # Version of your game
GAMEMODES: [] # ["solo"] or ["duo"] or ["solo", "duo"]
```

<u>*scoreboard.yaml content (only copy/paste)*</u>
```yaml
SOLO: # - username: Bobby score: 42
DUO: # - username: Bobby score: 42
```

You'll have to install everything you need on the EPIARCADE in the HUB with the allowance of a pedagogical member.  

If you mind getting HUB XP thanks to your game, you must firstly speak about it with a pedagological member.

# <u>Resources</u> #
As your game must be accessible, you can find some assets describing inputs, controls and others stuff by this link: [Epiarcade Assets](https://google.com).  

To test the inputs, you can try to plug one or both joystick(s) to your computer. Here are some input tester in differents languages: [Epiarcade Input Tester](https://google.com).

