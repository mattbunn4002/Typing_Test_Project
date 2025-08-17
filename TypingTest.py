import curses
import time
import menuState
import gameState
import gameMode

class TypingTest:
    DEFAULT_COLOUR_PAIR_ID = 1
    CORRECT_COLOUR_PAIR_ID = 2
    INCORRECT_COLOUR_PAIR_ID = 3
    DEFAULT_INVERTED_COLOUR_PAIR_ID = 4
    ESCAPE_KEY_UNICODE = 27

    def __init__(self, stdscr):
        curses.curs_set(False)
        self.loadColours()

        self.stdscr = stdscr
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)

        self.running = True
        self.gameMode = gameMode.GameMode.MENU
        self.menuState = menuState.MenuState()

    def loadColours(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def runMainGameLoop(self):
        while (self.running):
            self.handleInput()

            # Render the output to the screen
            self.renderScreen()

    def handleInput(self):
        try:
            key = self.stdscr.getch()
        except:
            key = None

        # Handle universal inputs first
        if (key == self.ESCAPE_KEY_UNICODE):
            self.running = False
            return
        elif (self.gameMode == gameMode.GameMode.MENU):
            self.handleMenuInput(key)
        elif (self.gameMode == gameMode.GameMode.PLAYING):
            self.handleGameplayInput(key)
        elif (self.gameState == 'postGame'):
            self.handlePostGameInput(key)

    def handleMenuInput(self, key):
        # Handle user pressing up or down
        if (key in [ord('s'), ord('S'), curses.KEY_DOWN]):
            self.menuState.currentIndex = min(self.menuState.currentIndex + 1, len(self.menuState.menuOptions) - 1) # Can refactor these into methods like "increaseIndex" on menuState that validates it's within bounds
        elif (key in [ord('w'), ord('W'), curses.KEY_UP]):
            self.menuState.currentIndex = max(0, self.menuState.currentIndex - 1)
        elif key in (ord('\n'), ord('\r'), curses.KEY_ENTER):
            if (self.menuState.currentIndex == self.menuState.menuOptions.index('Play')):
                # Play selected
                self.gameMode = gameMode.GameMode.PLAYING
                self.gameState = gameState.GameState(self.stdscr)
            elif (self.menuState.currentIndex == self.menuState.menuOptions.index('Options')):
                self.menuState = menuState.MenuState('options')
            elif (self.menuState.currentIndex == self.menuState.menuOptions.index('Achievements')):
                self.menuState = menuState.MenuState('achievements')
            elif (self.menuState.currentIndex == self.menuState.menuOptions.index('Exit')):
                self.running = False

    def renderScreen(self):
        if (self.gameMode == gameMode.GameMode.MENU and self.menuState.menuType == 'main'):
            self.renderMainMenu()
        elif (self.gameMode == gameMode.GameMode.PLAYING):
            self.renderGameplayScreen()
        elif (self.gameMode == gameMode.GameMode.MENU and self.menuState.menuType == 'options'):
            self.renderOptionsScreen()
        elif (self.gameMode == gameMode.GameMode.MENU and self.menuState.menuType == 'achievements'):
            self.renderAchievementsScreen()
        elif (self.gameMode == gameMode.GameMode.MENU and self.menuState.menuType == 'postGame'):
            self.renderPostGameScreen()

    def handleGameplayInput(self, key):
        gs = self.gameState
        if (key in [curses.KEY_BACKSPACE, ord('\b')]):
            if (len(gs.playerText) == 0):
                return
            # If player deleted a space character, decrement word count
            if (gs.playerText.pop() == ' '):
                gs.wordCount -= 1
        elif (len(gs.playerText) < len(gs.targetText) and key != -1):
            gs.playerText.append(chr(key))

        # Increment mistake count if required (latest char wrong and previous char not wrong)
        if (
            key not in (curses.KEY_BACKSPACE, ord('\b'), -1)
            and len(gs.playerText) > 0
            and gs.playerText[-1] != gs.targetText[len(gs.playerText) - 1]
            and (
                    len(gs.playerText) == 1
                    or gs.playerText[-2:-1][0] == gs.targetText[len(gs.playerText) - 2]
                )
            ):
            gs.mistakeCount += 1

        # If player inputted a space character, increment word count
        if (key in [ord(' ')]):
            gs.wordCount += 1

        gs.secondsElapsed = max(time.time() - gs.startTime, 1)
        gs.wpm = round(gs.wordCount / (gs.secondsElapsed / 60))

        if ("".join(gs.playerText) == gs.targetText):
            if (len(gs.remainingSentences) == 0):
                # The player finished all sentences
                self.gameMode = gameMode.GameMode.MENU
                self.menuState = menuState.MenuState('postGame')
                self.stdscr.nodelay(False)
            else:
                # Player finished a sentence
                gs.updateSentence()

    def handlePostGameInput(self, key):
        # Whenever any key pressed on post-game page we should just load the main menu
        self.menuState = menuState.MenuState('main')

    def renderMainMenu(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Typing speed test!\n", curses.color_pair(1))

        for index, optionText in enumerate(self.menuState.menuOptions):
            if index == self.menuState.currentIndex:
                self.stdscr.addstr(index + 2, 1, optionText, curses.color_pair(self.DEFAULT_INVERTED_COLOUR_PAIR_ID))
                self.stdscr.addstr(index + 2, 0, '>')
            else:
                self.stdscr.addstr(index + 2, 1, optionText)
    
    def renderPostGameScreen(self):
        gs = self.gameState
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Post game analysis!\n", curses.color_pair(1))
        self.stdscr.addstr(2, 0, f"Words per minute: {gs.wpm}")
        self.stdscr.addstr(3, 0, f"Time elapsed: {round(gs.secondsElapsed)}s")
        self.stdscr.addstr(4, 0, f"Mistakes made: {gs.mistakeCount}")
        self.stdscr.addstr(8, 0, f"Press any key to return to the main menu...")

    def renderGameplayScreen(self):
        gs = self.gameState
        self.stdscr.clear()

        # Display the underlay text
        self.stdscr.addstr(0, 0, gs.targetText)
        self.stdscr.addstr(2, 0, f'WPM: {str(gs.wpm)}')
        self.stdscr.addstr(3, 0, f'Time elapsed: {str(round(gs.secondsElapsed))}s')

        for i in range(len(gs.playerText)):
            # If each overlay character matches the underlay text then display it in green, otherwise red
            if gs.targetText[i] == gs.playerText[i]:
                color = curses.color_pair(self.CORRECT_COLOUR_PAIR_ID)
                self.stdscr.addstr(0, i, gs.playerText[i], color)
            else:
                color = curses.color_pair(self.INCORRECT_COLOUR_PAIR_ID)
                if (gs.targetText[i] == ' '):
                    self.stdscr.addstr(0, i, gs.playerText[i], color)
                else:
                    self.stdscr.addstr(0, i, gs.targetText[i], color)
        
        self.stdscr.addstr(4, 0, f'Mistakes: {str(gs.mistakeCount)}')

    def renderAchievementsScreen(self):
        self.stdscr.clear()
        