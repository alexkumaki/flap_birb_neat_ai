# flap_birb_neat_ai
Adding NEAT to a popular game


Neccessary Libraries:
 - pygame-ce (This uses the community edition of pygame, and will throw errors if using the standard version. All regular versions must be removed for this to run correctly.)
 - NEAT (This is the main library used for the AI.)


The idea of this project is to see if an AI can learn to play Flap Birb, a definitely original game that will not cause any sort of copyright infringement. It uses the NEAT algorithm and a few inputs to decide when the player should flap it's wings and bounce higher. The inputs it takes in are it's height on the screen, the distance to the next 'pipes', and the relative height of the gap between the upcoming 'pipes.' 

The AI seems to be quite effective, frequently reaching an unloseable state within the first few generations. This seems pretty reasonable, as the actions are incredibly repeatable and most humans only fail when they get bored or distracted. It is very possible to make the AI have a more difficult time though by changing a few settings, including the jump power or the gravity speed, which can have a much bigger effect on how well it does. Lag also is an issue in the beginning of each generation, although that may just be my personal computer having an issue with running 50 iterations simultaneously, and as more individuals die off the lag goes away. 

TODO: 
 - Add better graphics (or graphics at all)
 - Optimize to reduce lag
