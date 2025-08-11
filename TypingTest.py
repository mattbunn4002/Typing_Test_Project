import curses
import random

class TypingTest:
    DEFAULT_COLOUR_PAIR_ID = 1
    CORRECT_COLOUR_PAIR_ID = 2
    INCORRECT_COLOUR_PAIR_ID = 3
    INPUT_TEXT_FILE_NAME = 'sentences.txt'

    gameSentences = []

    def __init__(self, stdscr):
        self.loadColours()
        self.loadSentences()
        self.stdscr = stdscr

    def loadSentences(self):
        with open(self.INPUT_TEXT_FILE_NAME, 'r') as file:
            self.gameSentences = file.read().splitlines()

    def loadColours(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def renderText(self, underlayText, overlayText):
        # Display the underlay text
        self.stdscr.addstr(0, 0, underlayText, self.DEFAULT_COLOUR_PAIR_ID)

        for i in range(len(overlayText)):
            # If each overlay character matches the underlay text then display it in green, otherwise red
            if underlayText[i] == overlayText[i]:
                color = curses.color_pair(self.CORRECT_COLOUR_PAIR_ID)
                self.stdscr.addstr(0, i, overlayText[i], color)
            else:
                color = curses.color_pair(self.INCORRECT_COLOUR_PAIR_ID)
                if (underlayText[i] == ' '):
                    self.stdscr.addstr(0, i, overlayText[i], color)
                else:
                    self.stdscr.addstr(0, i, underlayText[i], color)
        

    def runGameRound(self):
        # Grab all of our sentences
        remainingSentences = self.gameSentences

        while (len(remainingSentences) > 0):
            self.stdscr.clear()
            # Grab a random sentence for the underlay from the ones available and then delete it from the remaining sentences
            i = random.randint(0, len(remainingSentences) - 1)
            underlayText = remainingSentences[i]
            del remainingSentences[i]
            overlayText = []

            # Display starting sentence
            self.renderText(underlayText, overlayText)

            # Start grabbing inputted keys and re-rendering underlay and overlay text each time
            while (True):
                key = self.stdscr.getkey()

                if (key in ("KEY_BACKSPACE", '\b', "\x7f")):
                    if (len(overlayText) == 0):
                        continue
                    overlayText.pop()
                    self.renderText(underlayText, overlayText)
                elif (len(overlayText) < len(underlayText)):
                    overlayText.append(key)
                    self.renderText(underlayText, overlayText)
                
                if ("".join(overlayText) == underlayText):
                    self.stdscr.clear()
                    self.stdscr.addstr("You finished the sentence! Press any key to proceed...")
                    self.stdscr.getkey()
                    self.stdscr.displayPostGameScreen()
                    break