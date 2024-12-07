from . import helpers
from .color import Color

class Scale:
    def __init__(self, c1, c2, domain=[0, 1]):
        self.c1 = c1
        self.c2 = c2
        assert c1.color_space == c2.color_space, "Both colors have to be in the same color space"
        self.color_space = c1.color_space
        self.domain = domain

    def __call__(self, value):
        values = []
        for i in range(3):
            values.append(self._interpolate(i, self._normalize(value)))

        return Color(values, self.color_space)

    def classes(self, n):
        classes = []
        for i in range(n):
            # Denormalize
            value = (i / (n - 1) * (self.domain[1] - self.domain[0]) + self.domain[0])
            color = self(value).to_rgb()
            classes.append(color)

        return classes

    def to_html(self, steps=100):
        return helpers.gradient_to_html(self.classes(steps))

    def _repr_html_(self):
        return self.to_html()

    def _interpolate(self, i, value):
        return self.c1[i] + value * (self.c2[i] - self.c1[i])

    def _normalize(self, value):
        return (value - self.domain[0]) / (self.domain[1] - self.domain[0])
