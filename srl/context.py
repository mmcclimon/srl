import curses
from srl.player import Player
from srl.keymap import Keymap

class UserQuit(Exception):
    pass

class Context:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(trace=True)
        self.keymap = Keymap()
        self._is_running = True

        self.drawables = set([ self.player ])
        self.screen.clear()

        # draw our lil debugging window
        self.cmd_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_win.addstr(0, 0, '[debug]')

        self.screen.refresh()
        self.cmd_win.refresh()

    @property
    def is_running(self):
        return self._is_running

    def loop_once(self):
        for thing in self.drawables:
            thing.draw(self)

        self.handle_input()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)


    def handle_input(self):
        k = self.screen.getkey()
        self.keymap.handle_key(self, k)

    def debug(self, msg):
        self.cmd_win.clear()
        self.cmd_win.addstr(0, 0, '[debug] ' + msg)
        self.cmd_win.refresh()


