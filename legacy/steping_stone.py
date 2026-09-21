def recall_game():
    # Get input from the user
    sentence = input("Enter a sentence: ")
    words = sentence.split()  # Split the sentence into words

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
            print(revealed_sentence)

            # Pause and then hide the sentence
            input("Memorize this part and press Enter to hide it...")

            # Clear the screen
            print("\n" * 100)  # Simulate screen clearing

            # Ask the user to recall the sentence so far
            recall = input("Recall the sentence so far: ")
            if recall.strip() == revealed_sentence:
                print("\nCorrect! Moving to the next level...")
                break  # Exit the loop and move to the next level
            else:
                print("\nOops! That's not correct.")
                print("Let's try this level again.")

    print("\nCongratulations! You recalled the entire sentence!")

# Run the game
recall_game()

# TODO: See if you can make an Apple Shortcut of this or something
# TODO: Make this but with a GUI and this thing for speaking not typing

# Just Try this mobility exercises, with Ne Me Quitte Pas
# Try with 5 Most information Sentences of something
# https://www.youtube.com/watch?v=47_zY0





