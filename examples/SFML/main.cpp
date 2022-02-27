#ifndef SFML_STATIC
#endif //SFML_SATIC

#pragma region includes
#include <SFML/Graphics.hpp>
#include <string>
#include <iostream>
#include <cstdlib>
#include "shape.h"
#pragma endregion includes

#pragma region variables
sf::RenderWindow window;
sf::RectangleShape rect;
int speed = 4;
#pragma endregion variables

int main()
{
    // Create window
    window.create(sf::VideoMode(800, 600), "Test Input");
    window.setFramerateLimit(60);

    rect = PB_Rect(10, 10, 32, 32);

    // While window is open
    while (window.isOpen()) {
        sf::Event event;
        // events
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Arcade joystick movement
        rect.move(sf::Joystick::getAxisPosition(0, sf::Joystick::Axis::X) / 100 * speed, speed * sf::Joystick::getAxisPosition(0, sf::Joystick::Axis::Y) / 100);

        // Arcade buttons
        
        if (sf::Joystick::isButtonPressed(0, 0)) {
            std::cout << "Bouton 1" << std::endl;
        }
        if (sf::Joystick::isButtonPressed(0, 1)) {
            std::cout << "Bouton 2" << std::endl;
        }
        if (sf::Joystick::isButtonPressed(0, 2)) {
            std::cout << "Bouton 3" << std::endl;
        }
        if (sf::Joystick::isButtonPressed(0, 3)) {
            std::cout << "Bouton 4" << std::endl;
        }
        if (sf::Joystick::isButtonPressed(0, 4)) {
            std::cout << "Bouton 5" << std::endl;
        }

        // Draw and update
        window.draw(rect);
        window.display();
        window.clear();
    }

    return 0;
}
