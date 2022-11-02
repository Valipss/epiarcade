# How to use #
1. Use ```make``` (same as ```make install_dependencies```) to install needed modules.

2. Use ```make run``` to launch the launcher and load the games.

3. The Launcher is now running, have fun.

# How to add a new game #

1. Create a directory named with the game's name inside the ```games/``` directory.

2. Create the 'config.yaml' file within the new directory. Its file must include required fields given in ```games/config_example.yaml```.

3. Add your executable file to the new directory.

4. Your game is now deployed, Enjoy!


sudo modprobe -r pn533_usb
python3 -m nfc -vvv