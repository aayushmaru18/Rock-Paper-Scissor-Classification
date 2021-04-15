import cv2
import numpy as np 
from random import choice

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
 
# loading the CNN model
model = load_model("rock_paper_scissors.h5")

cap = cv2.VideoCapture(0)

def calculate_winner(user, computer):

    if user == computer:
       return('Tie')

    if user == "rock":
        if computer == "scissors":
            return("User")
        if computer == "paper":
            return("Computer")

    if user == "paper":
        if computer == "rock":
            return "User"
        if computer == "scissors":
            return "Computer"      

    if user == "scissors":
        if computer == "paper":
            return("User")
        if computer == "rock":
            return("Computer")

# we are making a game of only 5 points
count = 0

user_score = 0
computer_score = 0

while(cap.isOpened()):
    
    ret, frame = cap.read()
    #frame = cv2.flip(frame, 1)

    # rectangle for user to play
    cv2.rectangle(frame, (100, 100), (500, 500), (0, 0, 255), 2)
    # rectangle for computer to play
    cv2.rectangle(frame, (800, 100), (1200, 500), (0, 0, 255), 2)

    # extract the region of image within the user rectangle
    roi = frame[100:500, 100:500]

    # deciding the move for computer
    computer_move = choice(['rock', 'paper', 'scissors'])

    if computer_move == 'rock':
        icon = cv2.imread("Testing/rock/testrock03-30.png")

    if computer_move == 'paper':
        icon = cv2.imread("Testing/paper/testpaper04-21.png")

    if computer_move == 'scissors':
        icon = cv2.imread("Testing/scissors/testscissors03-17.png")

    icon = cv2.resize(icon, (400, 400))
    #frame[100:500, 800:1200] = icon

    if cv2.waitKey(10) & 0xFF == ord('p'):

        # convert into the required dimension for Convolutional Neural Network
        # i.e. (1, 300, 300, 3)
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300,300))
        img = img_to_array(img)
        img = img.reshape(1, 300, 300, 3)

        predicted_class = model.predict_classes(img)

        # "'paper': 0, 'rock': 1, 'scissors': 2"

        if predicted_class[0] == 1:
            user_move = 'rock'

        elif predicted_class[0] == 0:
            user_move = 'paper'

        elif predicted_class[0] == 2:
            user_move = 'scissors'

        print(user_move)

        if predicted_class is not None:
            current_status = calculate_winner(user_move, computer_move)

            # update the individual scores
            if current_status == 'User':
                user_score += 1
            elif current_status == 'Tie':
                continue
            else:
                computer_score += 1

            print("Round {}: \n User={}-{} | Computer={}-{} \n".format(count, user_score, user_move, computer_score, computer_move))

        count += 1
        
        if count == 5:
            if user_score > computer_score:
                winner = "User"
            else:
                winner = "Computer"
            
            print('* * * * * * * * * * * *')
            print(f"{winner} has won the game !!!")
            print('* * * * * * * * * * * *')
    
    
    cv2.imshow('Rock Paper Scissors', frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()