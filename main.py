import curses
from curses import wrapper
import TypingTest

def main(stdscr):
    typingTest = TypingTest.TypingTest(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, "Typing speed test - Press any key to begin\n", curses.color_pair(1))
    stdscr.getkey()
    stdscr.refresh()
    typingTest.runGameRound()

wrapper(main)