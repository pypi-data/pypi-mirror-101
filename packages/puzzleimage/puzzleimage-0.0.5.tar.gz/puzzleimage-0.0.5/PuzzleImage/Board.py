import matplotlib.pyplot as plt
import numpy as np


class Board:
    def __init__(self, cell, blank):
        self.cell = cell
        self.blank = blank
        self.height, self.width = self.cell.shape

    def draw_board(self, ax):
        ax.axis("off")
        ax.set(aspect="equal", xlim=(0, self.width), ylim=(0, self.height))

        ax = self._draw_inner_lines(ax, self.cell)
        ax = self._draw_outer_lines(ax, self.cell, color="k", ls="-", lw=4, zorder=4)
        ax = self._draw_empty_cells(ax, self.cell, color="#f5efe6")
        return ax

    def _draw_inner_lines(self, ax, cell):
        left = (self.cell[:, :-1] != self.blank)
        right = (self.cell[:, 1:] != self.blank)
        top = (self.cell[:-1, :] != self.blank)
        bottom = (self.cell[1:, :] != self.blank)
        # thin
        thin_vline_x = np.where(left * right)[1] + 1
        thin_vline_y = self.height - 1 - np.where(left * right)[0]
        thin_hline_x = np.where(top * bottom)[1]
        thin_hline_y = self.height - 1 - np.where(top * bottom)[0]
        ax.plot([thin_vline_x, thin_vline_x], [thin_vline_y, thin_vline_y + 1], color="#EBEBEB", ls="-", lw=1)
        ax.plot([thin_hline_x, thin_hline_x + 1], [thin_hline_y, thin_hline_y], color="#EBEBEB", ls="-", lw=1)
        # bold
        draw_bold_vline = np.logical_or(~left * right, left * ~right)
        bold_vline_x = np.where(draw_bold_vline)[1] + 1
        bold_vline_y = self.height - 1 - np.where(draw_bold_vline)[0]
        draw_bold_hline = np.logical_or(~top * bottom, top * ~bottom)
        bold_hline_x = np.where(draw_bold_hline)[1]
        bold_hline_y = self.height - 1 - np.where(draw_bold_hline)[0]
        ax.plot([bold_vline_x, bold_vline_x], [bold_vline_y, bold_vline_y + 1], color="k", ls="-", lw=1, zorder=4)
        ax.plot([bold_hline_x, bold_hline_x + 1], [bold_hline_y, bold_hline_y], color="k", ls="-", lw=1, zorder=4)
        return ax

    def _draw_outer_lines(self, ax, cell, **kwargs):
        ax.plot([0, 0, self.width, self.width, 0], [0, self.height, self.height, 0, 0], **kwargs)
        return ax

    def _draw_empty_cells(self, ax, cell, color="#f5efe6"):
        cmap = plt.cm.viridis
        cmap.set_over(color, alpha=1)
        cmap.set_under("white", alpha=0)
        ax.imshow(self.cell == self.blank, extent=[0, self.width, 0, self.height], cmap=cmap, vmin=0.49, vmax=0.51)
        return ax

    def draw_answer(self, ax, cell, **kwargs):
        for i in range(self.height):
            for j in range(self.width):
                x = j + 0.5
                y = self.height - i - 0.6
                rotation = 0
                # The rotation process for vertical long tones
                if self.cell[i, j] == "ー" and j >= 1 and self.cell[i, j - 1] == self.blank:
                    x += 0.01
                    y += 0.15
                    rotation = 90
                kwargs["rotation"] = rotation
                ax.text(x, y, self.cell[i, j], **kwargs)
        return ax
