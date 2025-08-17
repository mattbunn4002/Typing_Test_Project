import curses
from curses import wrapper
import TypingTest

def main(stdscr):
    typingTest = TypingTest.TypingTest(stdscr)
    typingTest.runMainGameLoop()

wrapper(main)