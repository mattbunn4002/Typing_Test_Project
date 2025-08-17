class MenuState:
    def __init__(self, menuType = 'main', menuOptions = ['Play', 'Options', 'Achievements', 'Exit']):
        self.currentIndex = 0
        self.menuOptions =  menuOptions
        self.menuType = menuType