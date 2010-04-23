import subprocess
from hashlib import md5

from django.conf import settings
from django import template
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

register = template.Library()

fs = FileSystemStorage()


def normalize_svg_path(data, box, size):
    """
    Resize the path to fit frame

    The original paths are too big and result in
    the SVG not being displayed.

    This function normalizes the size of every path.
    """
    # parse box data
    x0, y0, w, h = [float(f) for f in box.split(' ')]

    # find resize factor
    xf = size[0] / w
    yf = size[1] / h
    factor = min(xf, yf)

    # harvest the SVG path and convert coords
    new_path = []
    xs = []
    ys = []
    factor = xf
    is_lon = True
    for chunk in data.split(' '):
        try:
            # chunk is a coord
            chunk = float(chunk) * factor
        except ValueError:
            pass
        else:
            if is_lon:
                xs.append(float(chunk))
                is_lon = False
            else:
                ys.append(float(chunk))
                is_lon = True
            chunk = "%f" % chunk
        finally:
            new_path.append(chunk)

    # recalculate box for better precision
    box = "%f %f %d %d" % (min(xs),
                           min(ys),
                           abs(max(xs) - min(xs)),
                           abs(max(ys) - min(ys)),)

    return {'path': ' '.join(new_path), 'box': box}



def to_svg(country):
    """
    Creates an SVG picture of the country and returns its URL.

    {% load map_tags %}

    {{ object|svg_map }}
    """

    # keep countries anonymous
    path = "svg/%s.svg" % md5(country.name.encode('utf-8')).hexdigest()

    # create SVG only once
    if not fs.exists(path):

        x0, y0, x1, y1 = country.geom.extent

        # svg Y axis is inverted
        y0, y1 = -1 * y0, -1 * y1

        # view box
        box = "%f %f %f %f" % (min(x0, x1),
                               min(y0, y1),
                               abs(x0 - x1),
                               abs(y0 - y1))


        svg_data = normalize_svg_path(country.svg, box, (400, 400))

        # inject vector data into template
        svg_string = render_to_string('worldgame/template.svg', svg_data)

        svg_path = fs.save(path, ContentFile(svg_string.encode('utf-8')))


    return fs.url(path)

register.filter('svg_map', to_svg)
