from PuzzleImage.Board import Board
from PuzzleImage.PuzzleImage import PuzzleImage
from PuzzleImage.WordList import WordList


class SkeltonImage(PuzzleImage):
    def __init__(self, blank="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blank = blank

    def get_board(self, ax, cell, title=None, w_count=None, is_answer=False):
        """
        Create a puzzle board axes.
        
        Parameters
        ----------
        ax : matplotlib.pyplot.axes
            Axes to be plotted.
        cell : numpy ndarray
            Puzzle board.
        title : str, default ""
            Puzzle name.
        is_answer : bool, default False
            If True, draw with the answer.
        """
        board = Board(cell, self.blank)
        ax = board.draw_board(ax)
        if title:
            ax = self._draw_title(ax, title, x=0.1, y=board.height + 0.2, size=16, ha="left", color="#1a1a1a")
        if w_count:
            ax = self._draw_title(ax, f"{w_count}語", x=board.width, y=board.height + 0.1, size=12, ha="right",
                                  color="#1a1a1a")
        if is_answer:
            ax = board.draw_answer(ax, cell, size=18, ha="center", va="center")
        return ax

    def _draw_title(slef, ax, title, x, y, **kwargs):
        ax.text(x, y, str(title), **kwargs)
        return ax

    def _draw_word_count(slef, ax, count, x, y, **kwargs):
        ax.text(x, y, str(count), **kwargs)
        return ax

    def get_wordlist(self, ax, words, width, height, size):
        wl = WordList(words, width, height, size)
        ax = wl.draw_wordlist(ax)
        return ax
