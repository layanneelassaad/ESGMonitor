def dict_to_css_style(style):
    return ';'.join(['{}: {}'.format(key, val) for key, val in style.items()])


def gradient_to_html(gradient, width=300, height=30):
    div_style = {
        'position': 'relative',
        'width': '{}px'.format(width)
    }
    # TODO add a HTML class
    div = '<div style="{}">{}</div>'
    span_width = 100 / len(gradient)

    spans = []
    for color in gradient:
        span_style = {
            'display': 'inline-block',
            'height': '{}px'.format(height),
            'width': '{}%'.format(span_width),
            'background-color': color
        }
        span = '<div style="{}"></div>'.format(dict_to_css_style(span_style))
        spans.append(span)

    return div.format(dict_to_css_style(div_style), ''.join(spans))
