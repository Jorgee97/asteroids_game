# Space Asteroids PyGame
A little space invaders like game, build with pygame

# Screenshots
![Alt Text](screenshots/game.gif)

The game runs at ~60fps (Lag on the game is on the gif capture)

# Features
I implemented the game using an object oriented approach, I may have failed in some concerns but that was the objective

- Sprites were created by me (first time) using Aseprite
- The game implements pixel perfect collisions using the pygame.sprite methods
- Sound effects by sfxr

# How to run
- Create a virtual environment and activate it
```
# Windows
py -m venv .env
\.env\Scripts\activate

# Unix
python3 -m venv .env
source .env/bin/activate

```
- Install the necessary packages
```
pip install -r requirements.txt
```

- Run the program
```
python game.py
```







