import random
import time

class GameState:
    INPUT_TEXT_FILE_NAME = 'sentences.txt' # Can change this to a var for different diffulty text files in future

    def __init__(self, stdscr):
        self.gameSentences = self.remainingSentences = self.getSentences()
        self.updateSentence()
        self.playerText = []
        # Start at 1 because the number of words is number of spaces + 1
        self.wordCount = 1
        self.wpm = 0
        self.secondsElapsed = 0
        self.mistakeCount = 0
        self.startTime = time.time()
        stdscr.nodelay(True)

    def getSentences(self):
        with open(self.INPUT_TEXT_FILE_NAME, 'r') as file:
            return file.read().splitlines()
        
    def updateSentence(self):
        # Grab a random sentence as the target from the ones available and then delete it from the remaining sentences
        i = random.randint(0, len(self.remainingSentences) - 1)
        self.targetText = self.remainingSentences[i]
        del self.remainingSentences[i]
        self.playerText = []