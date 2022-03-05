#include <SFML/Graphics.hpp>

sf::RectangleShape PB_Rect(int posX, int posY, int width, int height)
{
    sf::RectangleShape rect (sf::Vector2f(width, height));
    rect.setPosition(posX, posY);
    rect.setFillColor(sf::Color(255, 0, 0, 255));
    return rect;
}