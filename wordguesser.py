import random
from datetime import date
from wordlist import wordlist as wordlist

def wordguesser():
    def wordprogress():
        progress = ""
        for i in currentword:
            if i in guessedletters:
                progress += i
            else:
                progress += "_"
        return progress

    def hintfunc():
        while hint:
            h = random.randint(0,length-1)
            if currentguess[h] == "_":
                letter = currentword[h]
                print(f"{spacing}Your hint is '{letter}'")
                return letter, False

    def wrongguess():
        print(f"{spacing}{letter} is not in this word. ",end="")
        if wrongletters == mistakes:
            print("You can make no more mistakes")
        elif wrongletters > mistakes:
            print(f"Out of tries, {'good luck on the next word.' if len(wordstoplay) > 0 else 'thanks for playing'}")
        else:
            print(f"You have made {wrongletters}/{mistakes} mistakes")

    def endword():
        if wrongletters == limitmistakes:
            print(f"The word was {currentword}")
            wrongwords.append(currentword)
        if "_" not in currentguess:
            print(f"{currentword}  Well done.")
            correctwords.append(currentword)

    def highscore():
        if mode:
            points = len(correctwords) * 100 - totalhelp * 5 - totalguesses
            saveto = f"score{mode}.txt"
            with open (saveto, 'a') as f:
                f.write(f'\n{name}|{points}|{len(correctwords)}|{totalguesses-totalhelp}|{totalmistakes}|{totalhelp}|{date.today()}')

    def results():
        if willtoplay:
            print(f"\nYou have finished the game. Here's your score:")
            print(f"{len(correctwords)} of {rounds} words guessed correctly.")
            print(f"In total you made {totalguesses - totalhelp} guesses of which {totalmistakes} {f'was' if totalmistakes == 1 else 'were'} wrong.")
            print(f"You asked for {totalhelp} {'hint' if totalhelp==1 else 'hints'}.")
            highscore()
        else:
            print(f"\nYou have quit the game early. The word you gave up on was {currentword}.") 
            print(f"You guessed {len(correctwords)} out of {len(correctwords + wrongwords)} correctly.")
            remainingrounds = rounds - len(correctwords + wrongwords)
            print(f"There {'was 1 round' if remainingrounds == 1 else 'were '+str(remainingrounds)+' rounds'} left to play.")

    # Welcome message and asking for name and game settings.
    name = input("Welcome to Word Guesser. What's your name?\n").title()
    print(f"\nHighscores are kept for games with 10 rounds in easy, normal or hard mode.")
    gamechoice = input(f"Would you like to play [e]asy, [N]ormal or [h]ard mode or [c]hoose your own settings? ").lower()
    gamemodes = {"e":[1,10,7,"easy"],"n":[2,10,5,"normal"],"h":[3,10,3,"hard"]}
    if len(gamechoice) == 0:
        gamechoice = "n"
    if gamechoice[0] in ("e", "n", "h"):
        mode = gamemodes[gamechoice][0]
        rounds = gamemodes[gamechoice][1]
        mistakes = gamemodes[gamechoice][2]
        print(f"You'll be playing 10 rounds in {gamemodes[gamechoice][3]} mode. You can make {mistakes} mistakes per word.")
    else:
        mode = False
        while True:
            try: 
                rounds = int(input("How many rounds do you want to play? "))
                if 0 < rounds < len(wordlist):
                    break
                else:
                    print(f"Enter a value between 0 and {len(wordlist)+1}")
            except ValueError: 
                print(f"Enter a value")
        while True:
            try:
                mistakes = int(input("How many mistakes are allowed per word? "))
                if mistakes > 0:
                    break
                elif mistakes <= 0:
                    mistakes = 0
                    print("No mistakes allowed. Good luck...")
                    break
            except ValueError:
                print("Enter a value")
    
    # Setting up the list of words to play and required variables.
    wordstoplay = []
    numbers = random.sample(range(0,len(wordlist)),rounds)
    for i in numbers:
        wordstoplay.append(wordlist[i])
    limitmistakes = mistakes + 1
    correctwords = []
    wrongwords = []
    totalmistakes = 0
    totalguesses = 0 
    totalhelp = 0
    willtoplay = True

    print(f"\nEnter '?' to see guessed letters, 'help' to get a hint, 'quit' to end the game.")
    while len(wordstoplay) > 0 and willtoplay is True:
        currentword = wordstoplay.pop()
        wrongletters = 0
        guessedletters = []
        hint = True
        length = len(currentword)
        spacing = (length + 2) * " "
        currentguess = wordprogress()
        if rounds > 10 and len(correctwords + wrongwords) % 5 == 0 and totalguesses > 0:
                print(f"\nYou have played {len(correctwords + wrongwords)} rounds. {len(wordstoplay)+1} more to go.")
        print(f"\nLet's play")
        # This while loop goes over the words in the wordstoplay list
        while wrongletters != limitmistakes and "_" in currentguess:
            letter = input(f"{currentguess}  Take a guess: ")
            letter = letter.lower()
            # Process assistive inputs
            if len(letter) != 1 or letter.isalpha() is not True:
                if letter == "?":
                    guessedletters.sort()
                    print(spacing,", ".join(guessedletters))
                    continue
                elif letter == "quit":
                    willtoplay = False
                    break 
                elif letter == "help":
                    if hint:
                        totalhelp += 1
                        letter, hint = hintfunc()
                    else:
                        print(f"{spacing}You have already received a hint for this word")
                        continue
                # Allow player to take a guess at the current word instead of guessing a letter.
                elif len(letter) == length:
                    if letter == currentword:
                        currentguess = currentword
                        totalguesses += 1
                    else:
                        print(f"{spacing}Nice try, but {letter} is not correct.")
                        totalguesses += 1
                        wrongletters += 1
                else:
                    print(f"{spacing}Please enter a single letter, guess for this word, '?', 'help' or 'quit'.")
                    continue
            # Process a guessed letter or the result from help.
            if len(letter) == 1:
                if letter not in guessedletters:
                    guessedletters.append(letter)
                    if letter in currentword:
                        currentguess = wordprogress()
                    else:
                       wrongletters += 1
                       wrongguess()
                else:
                    print(f"{spacing}{letter} has already been guessed")
            # Check if conditions are met for finishing this round.
            if wrongletters == limitmistakes or "_" not in currentguess:
                endword()
                totalguesses += len(guessedletters)
                totalmistakes += wrongletters
    results()
    if willtoplay is True:
        repeat = input("\nWould you like to play again? [y/N] ")
        if repeat == "y":
            print("\n")
            wordguesser()

if __name__ == '__main__':
    wordguesser()
