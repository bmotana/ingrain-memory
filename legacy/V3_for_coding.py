
x = """
plt.figure(figsize=(9, 5))
sns.set_style("whitegrid")
sns.regplot(x="Age",y="Salary", data=df)
plt.xlim(27, 42)
plt.ylim(60000,95000)
plt.legend(["ALL"])
plt.show()
"""

def recall_game():
    # Get input from the user
    # sentence = input("Enter a sentence: ")
    # words = sentence.replace("\n", " ") .split() # Split the sentence into words

    print("Enter multiple lines of input. Type 'END' to finish:")
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    print("\nWelcome to the Recall Game!")
    print("Try to recall the sentence as words are revealed one by one.")
    print("You must recall all words on each level to proceed to the next.")
    print(f"There will be {len(lines)} levels.")
    print("Press Enter to start.")

    input()  # Wait for the user to press Enter

    revealed_sentence = []  # Initialize the revealed sentence
    show_sentence = []
    #TODO: turn the variable into a list
    for i, test_line in enumerate(lines):
        # Append the new word to the revealed sentence
        show_sentence.append(test_line)
        test_line = test_line.strip()
        revealed_sentence.append(test_line)
        # print(revealed_sentence, "revealed_Sentences") # Debugging
        while True:  # Keep the player on the current level until they succeed


            # Display the revealed sentence
            print(f"\nLevel {i + 1}:")
            # print("\n".join(revealed_sentence))
            print("\n".join(show_sentence))

            # Clear the screen
            # print("\n" * 20)  # Simulate screen clearing

            # Pause and then hide the sentence
            input("Memorize this part and press Enter to hide it...")

            # Clear the screen
            print("\n" * 100)  # Simulate screen clearing

            # Ask the user to recall the sentence so far
            print("Recall the sentence so far: ")
            # TODO: do something about this input
            recall_lines = []
            while True:
                recall_line = input()
                if recall_line == "END":
                    break
                recall_line.replace("\t", "")
                recall_lines.append(recall_line)
            # TODO: change how this checks the input
            print(recall_lines, "recall_lines") # Debugging
            recall_lines = list(map(lambda x: x.replace("\t", ""), recall_lines))
            print(revealed_sentence, "revealed_Sentences")  # Debugging
            if recall_lines == revealed_sentence:
                print("\nCorrect! Moving to the next level...")
                break  # Exit the loop and move to the next level
            elif "q" in recall_lines:
                print("\nQuitting the game...")
                quit()
            else:
                print("\nOops! That's not correct.")
                print("Let's try this level again.")

    print("\nCongratulations! You recalled the entire sentence!")

# Run the game
try:
    recall_game()
except KeyboardInterrupt:
    print("\nGame interrupted by the user.")


