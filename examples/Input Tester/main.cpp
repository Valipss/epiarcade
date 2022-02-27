#include <SFML/Graphics.hpp>
#include <iostream>

#define btnWidth  64
#define btnHeight 40

#define joyWidth  64
#define joyHeight 64

#define joyAmpli  15
#define joySpace  ((2 * joyAmpli) + joyHeight)
#define textSize  40

#define scrWidth  800
#define scrHeight 600

static const sf::IntRect btnUp    = {       0, 0, btnWidth, btnHeight};
static const sf::IntRect btnDown  = {btnWidth, 0, btnWidth, btnHeight};

static const sf::IntRect joyFront = {       0, 0, joyWidth, joyHeight};
static const sf::IntRect joyBack  = {joyWidth, 0, joyWidth, joyHeight};

#define Player1 0

struct Joystick
{
    const std::string           latStr;
    const std::string           vertStr;
    const sf::Joystick::Axis    latAxis;
    const sf::Joystick::Axis    vertAxis;
};

static const Joystick joyDatas[] = {
    {   "X:",    "Y:",    sf::Joystick::Axis::X,    sf::Joystick::Axis::Y},
    {   "Z:",    "R:",    sf::Joystick::Axis::Z,    sf::Joystick::Axis::R},
    {   "U:",    "V:",    sf::Joystick::Axis::U,    sf::Joystick::Axis::V},
    {"PovX:", "PovY:", sf::Joystick::Axis::PovX, sf::Joystick::Axis::PovY}
};

void printJoystick(sf::RenderWindow &window, sf::Sprite &joySprite, sf::Text text, int joyIdx)
{
    if (joyIdx >= 4)
        return;
    joySprite.setTextureRect(joyBack);
    joySprite.setPosition(joyAmpli + ((scrHeight / 1.5) * (joyIdx % 2)), joyAmpli + joySpace * (joyIdx / 2));
    window.draw(joySprite);
    joySprite.setTextureRect(joyFront);
    joySprite.setPosition((joyAmpli + ((scrHeight / 1.5) * (joyIdx % 2))) + sf::Joystick::getAxisPosition(Player1, joyDatas[joyIdx].latAxis) * joyAmpli / 100, (joyAmpli + joySpace * (joyIdx / 2)) + sf::Joystick::getAxisPosition(Player1, joyDatas[joyIdx].vertAxis) * joyAmpli / 100);
    window.draw(joySprite);
    text.setPosition(joySpace + ((scrHeight / 1.5) * (joyIdx % 2)), joySpace * (joyIdx / 2));
    text.setString(joyDatas[joyIdx].latStr + std::to_string(sf::Joystick::getAxisPosition(Player1, joyDatas[joyIdx].latAxis)));
    window.draw(text);
    text.setPosition(joySpace + ((scrHeight / 1.5) * (joyIdx % 2)), joySpace - textSize + joySpace * (joyIdx / 2));
    text.setString(joyDatas[joyIdx].vertStr + std::to_string(sf::Joystick::getAxisPosition(Player1, joyDatas[joyIdx].vertAxis)));
    window.draw(text);
}

void printButtons(sf::RenderWindow &window, sf::Sprite &btnSprite)
{
    unsigned int fRow = sf::Joystick::getButtonCount(Player1) / 2;
    unsigned int sRow = sf::Joystick::getButtonCount(Player1) - fRow;

    for (unsigned int idx = 0; idx < sf::Joystick::getButtonCount(Player1); idx++) {
        if (sf::Joystick::isButtonPressed(Player1, idx)) {
            btnSprite.setTextureRect(btnDown);
        } else {
            btnSprite.setTextureRect(btnUp);
        }
        if (idx < fRow)
            btnSprite.setPosition(((scrWidth / fRow) - (btnWidth / fRow)) * idx + scrWidth / (fRow * 2), joyAmpli + joySpace + btnHeight * 3);
        else
            btnSprite.setPosition(((scrWidth / fRow) - (btnWidth / fRow)) * (idx - fRow) + scrWidth / (fRow * 2), joyAmpli + joySpace + btnHeight * 5);
        window.draw(btnSprite);
    }
}

int main(void)
{
    sf::RenderWindow window(sf::VideoMode(scrWidth, scrHeight), "SFML window");

    sf::Texture btnText;
    if (!btnText.loadFromFile("tstButton.png"))
        return (84);

    sf::Sprite btnSprite;
    btnSprite.setTexture(btnText);

    sf::Texture joyText;
    if (!joyText.loadFromFile("tstJoystick.png"))
        return (84);

    sf::Sprite joySprite;
    joySprite.setTexture(joyText);

    sf::Font font;
    if (!font.loadFromFile("arial.ttf"))
        return (84);

    sf::Text text;
    text.setFont(font);
    text.setCharacterSize(textSize);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        if (sf::Joystick::isConnected(Player1)) {
            printButtons(window, btnSprite);
            printJoystick(window, joySprite, text, 0);
            printJoystick(window, joySprite, text, 1);
            printJoystick(window, joySprite, text, 2);
            printJoystick(window, joySprite, text, 3);
            text.setString(sf::Joystick::getIdentification(Player1).name + ":" + std::to_string(sf::Joystick::getIdentification(Player1).productId) + ":" + std::to_string(sf::Joystick::getIdentification(Player1).vendorId));
            text.setCharacterSize(textSize / 2);
            text.setPosition(0, scrHeight - textSize);
            window.draw(text);
            text.setCharacterSize(textSize);
        }
        window.display();
        window.clear();
    }

    return (0);
}