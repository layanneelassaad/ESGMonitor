from . import conversions
from . import helpers

FORMATS = {
    'rgb': 'rgb({:.0f}, {:.0f}, {:.0f})',
    'lab': 'lab({:.3f}, {:.3f}, {:.3f})'
}

# TODO add RGB and LAB classes
class Color:
    def __init__(self, values, color_space='rgb'):
        self.values = values
        self.color_space = color_space

    def to_lab(self):
        color_space = 'lab'
        convert = self._get_converter(self.color_space, color_space)
        return Color(convert(self.values), color_space=color_space)

    def to_rgb(self):
        color_space = 'rgb'
        convert = self._get_converter(self.color_space, color_space)
        return Color(convert(self.values), color_space=color_space)

    def to_string(self):
        return FORMATS[self.color_space].format(*list(self.values))

    def to_html(self, width=30, height=30):
        div_style = {
            'width': '{}px'.format(width),
            'height': '{}px'.format(height),
            'background-color': self.to_rgb().to_string()
        }
        div = '<div style="{}"></div>'.format(helpers.dict_to_css_style(div_style))
        return div

    def _get_converter(self, a, b):
        return getattr(conversions, '2'.join([a, b]))

    def _repr_html_(self):
        return self.to_html()

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __getitem__(self, i):
        return self.values[i]
