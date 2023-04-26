import random  
import time  
import speech_recognition as sr  

# Define a function to recognize speech from microphone input
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    # Use the microphone as a source for audio input
    with microphone as source:
        # Adjust for ambient noise to reduce background noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio input from the microphone
        audio = recognizer.listen(source)
        
        # Initialize a dictionary to store the speech recognition results
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        
        try:
            # Attempt to transcribe the audio input using Google's speech recognition API
            response["transcription"] =  recognizer.recognize_google(audio)
        except sr.RequestError:
            # If the API is unavailable, set the "success" flag to False and store the error message
            response["success"] = False
            response["error"] = "API unavaliable"
        except sr.UnknownValueError:
            # If the audio cannot be transcribed, store the error message
            response["error"] = "Unable to recognize speech"
            
        # Return the response dictionary
        return response
    
if __name__ == "__main__":
    # Define a list of words and the number of guesses allowed
    WORDS = ['tiger', 'banana', 'orange', 'plant', 'mango']
    NUM_GUESSES = 3
    PROMPT_LIMIT = 4
    
    # Initialize a recognizer and a microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Choose a random word from the list
    word = random.choice(WORDS)
    
    # Print instructions for the game
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)
    print(instructions)
    time.sleep(3)  # Introduce a delay to give the user time to read the instructions
    
    # Initialize counters for correct and incorrect answers
    correct_answers = 0
    incorrect_answers = 0
    
    # Loop over the number of guesses allowed
    for i in range(NUM_GUESSES):
        # Loop over the number of prompts allowed
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak...'.format(i+1))
            # Call the recognize_speech_from_mic function to get the user's speech input
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break  # If a transcription is obtained, exit the loop
            if not guess["success"]:
                break  # If an error occurs, exit the loop
            print("I didn't catch that. What did you say?\n")
            
        # Check for errors in the guess dictionary
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        
        print("You said: {}".format(guess["transcription"]))
        
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1
        
        # If correct answer is given, remove selected word from list and choose another secret word
        if guess_is_correct:
            print("Correct!")
            correct_answers += 1
            WORDS.remove(word)
            if correct_answers == 2:
                print("You win!") # If user gets 2 correct answer print this
                break
            word = random.choice(WORDS)
            #
        else:
            print("Incorrect.")
            incorrect_answers += 1
            if incorrect_answers == 2:
                print("Sorry, you lose!\nI was thinking of '{}'.".format(word)) # If user gets 2 incorrect answer print this
                break
            
        if user_has_more_attempts:
            print("Try again.\n")
