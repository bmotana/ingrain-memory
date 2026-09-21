import time

def recall_game():
    # Get input from the user
    sentence = input("Enter a sentence: ")
    words = sentence.replace("\n", " ") .split() # Split the sentence into words

    print("\nWelcome to the Recall Game!")
    print("Try to recall the sentence as words are revealed one by one.")
    print("You must recall all words on each level to proceed to the next.")
    print(f"There will be {len(words)} levels.")
    print("Press Enter to start.")

    input()  # Wait for the user to press Enter

    revealed_sentence = ""  # Initialize the revealed sentence
    for i, word in enumerate(words):
        # Append the new word to the revealed sentence
        revealed_sentence = f"{revealed_sentence} {word}".strip()

        while True:  # Keep the player on the current level until they succeed

            # Display the revealed sentence
            print(f"\nLevel {i + 1}:")
            # print()
            print(revealed_sentence)
            time.sleep(5)
            # input("Look at the word(s): Press Enter to Continue.")

            # Clear the screen
            print("\n" * 20)  # Simulate screen clearing

            # Pause and then hide the sentence
            input("Say the Words, Press Enter to Check Your Answer.")

            # Clear the screen
            print("\n" * 20)  # Simulate screen clearing

            print(revealed_sentence)
            response = input("That you say these words Right \nPress N if you got it right or Just Press Enter to Try Again Press Q to quit \n")
            if response.lower().strip() == "n":
                print("\nCorrect! Moving to the next level...")
                print("\n" * 10)
                break # Exit the loop and move to the next level
            elif response.lower().strip() == "q":
                print("\nQuitting the game...")
                quit()
            else:
                print("\nOops! That's not correct.")
                print("Let's try this level again.")
                print("\n" * 10)

    print("\nCongratulations! You recalled the entire sentence!")

# Run the game
recall_game()