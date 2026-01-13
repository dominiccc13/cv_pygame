## About this project: ##

There are four files that will be utilized. They are: 
 - game.py
 - main.py
 - bg.jpg 
 - hand_landmarker.task
 - requirements.txt

game.py hosts a small socket server on your local machine on port 3000. main.py
will send commands via this socket to the game, that will interpret the commands 
as movement that will update the position of the 'player' rectangle. 

I have added a repeating background from the jpg file bg.jpg that is updated
based on the position of the player rectangle. 

hand_landmarker.task is the file that has trained the landmark functionality. It prevents a significant amount of load time from executing upon launching of the main.py script. 

requirements.txt contains the libraries used in the code.

## Testing the Program ##

You will need to install the libraries found in the requirements.txt file for Python 3.10. 

Once this is done, all that is necessary to test this project is to download, unzip, and run main.py and game.py. Two open hands with palms facing the camera will move forward. With the left hand higher than the right hand, the character will move forward and left. With just the left hand, the character will move left only. Same for the right hand. When fists are used instead of open hands, the rectangle will "sprint". 