from manim import *


__all__ = ["GridAxes"]


class GridAxes(Axes):
    def __init__(
        self,
        x_range=(-10, 10, 1),
        y_range=(-10, 10, 1),
        x_length=5,
        y_length=5,
        dashed_grid=False,
        grid_kw = None,
        tips=False,
        **kwargs
    ):
        super().__init__(x_range=x_range, y_range=y_range, x_length=x_length,  y_length=y_length, tips=tips, **kwargs)
        if grid_kw is None:
            grid_kw = dict()
        self.add_to_back(self.get_grid(dashed=dashed_grid, **grid_kw))

    def get_grid(self, dashed=False, **grid_kw):
        x_range, y_range = self.x_range, self.y_range
        x_min, x_max, x_step = x_range[0], x_range[1], x_range[2]
        y_min, y_max, y_step = y_range[0], y_range[1], y_range[2]
        x_ticks = np.arange(x_min, x_max + 2 * x_step, x_step)
        y_ticks = np.arange(y_min, y_max + y_step, y_step)

        grid = self.get_axes()
        line_class = {False: Line, True: DashedLine}[dashed]
        if grid_kw.get("stroke_width") is None:
            grid_kw["stroke_width"] = 1
        if grid_kw.get("stroke_opacity") is None:
            grid_kw["stroke_opacity"] = 0.5
        for x in x_ticks:
            line = line_class(
                self.coords_to_point(x, y_min),
                self.coords_to_point(x, y_max),
                **grid_kw
            )
            if x == 0:
                line.set_stroke(opacity=0)
            grid.add(line)
        for y in y_ticks:
            grid.add(line_class(
                self.coords_to_point(x_min, y),
                self.coords_to_point(x_max, y),
                **grid_kw
            ))
            if y == 0:
                line.set_stroke(opacity=0)
        return grid