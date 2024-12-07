# D65
XYZ_REFERENCE_NUMBERS = [95.047, 100.000, 108.883]


# See https://github.com/d3/d3-color/tree/master/test

# sRGB to LAB

def rgb2rgb(rgb):
    return rgb


def rgb2lab(rgb):
    xyz = rgb2xyz(rgb)
    lab = xyz2lab(xyz)
    return lab


def rgb2xyz(rgb):
    # rgb = rgb / 255
    # linear = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    # linear *= 100
    # coeff = [
    #     [0.4124564, 0.3575761, 0.1804375],
    #     [0.2126729, 0.7151522, 0.0721750],
    #     [0.0193339, 0.1191920, 0.9503041]
    # ]
    # xyz = np.dot(coeff, linear)

    rgb = [val / 255 for val in rgb]
    linear = [((val + 0.055) / 1.055) ** 2.4 if val > 0.04045 else val / 12.92 for val in rgb]
    linear = [val * 100 for val in linear]

    x = 0.4124564 * linear[0] + 0.3575761 * linear[1] + 0.1804375 * linear[2]
    y = 0.2126729 * linear[0] + 0.7151522 * linear[1] + 0.0721750 * linear[2]
    z = 0.0193339 * linear[0] + 0.1191920 * linear[1] + 0.9503041 * linear[2]
    xyz = [x, y, z]

    return xyz


def xyz2lab(xyz):
    # var = xyz / XYZ_REFERENCE_NUMBERS
    # var = np.where(var > 0.008856, var ** (1 / 3), (7.787 * var) + (16 / 116))

    var = [val / ref for val, ref in zip(xyz, XYZ_REFERENCE_NUMBERS)]
    var = [val ** (1 / 3) if val > 0.008856 else (7.787 * val) + (16 / 116) for val in var]

    L = (116 * var[1]) - 16
    a = 500 * (var[0] - var[1])
    b = 200 * (var[1] - var[2])
    lab = [L, a, b]

    return lab


# LAB to sRGB

def lab2lab(lab):
    return lab


def lab2rgb(lab):
    xyz = lab2xyz(lab)
    rgb = xyz2rgb(xyz)
    return [round(val) for val in rgb]


def lab2xyz(lab):
    # var_y = (lab[0] + 16) / 116
    # var_x = lab[1] / 500 + var_y
    # var_z = var_y - lab[2] / 200
    #
    # var_xyz = np.array([var_x, var_y, var_z])
    # var_xyz = np.where(var_xyz ** 3 > 0.008856, var_xyz ** 3, (var_xyz - 16 / 116) / 7.787)
    # xyz = var_xyz * XYZ_REFERENCE_NUMBERS

    var_y = (lab[0] + 16) / 116
    var_x = lab[1] / 500 + var_y
    var_z = var_y - lab[2] / 200
    var_xyz = [var_x, var_y, var_z]

    var_xyz = [var ** 3 if var ** 3 > 0.008856 else (var - 16 / 116) / 7.787 for var in var_xyz]
    xyz = [var * ref for var, ref in zip(var_xyz, XYZ_REFERENCE_NUMBERS)]

    return xyz


def xyz2rgb(xyz):
    # var_xyz = xyz / 100
    #
    # coeff = [
    #     [3.2404542, -1.5371385, -0.4985314],
    #     [-0.9692660, 1.8760108, 0.0415560],
    #     [0.0556434, -0.2040259, 1.0572252]
    # ]
    # var_rgb = np.dot(coeff, var_xyz)
    #
    # var_rgb = np.where(var_rgb > 0.0031308, 1.055 * (np.power(var_rgb, (1 / 2.4))) - 0.055, 12.92 * var_rgb)
    # rgb = var_rgb * 255

    var_xyz = [val / 100 for val in xyz]

    var_r = 3.2404542 * var_xyz[0] - 1.5371385 * var_xyz[1] - 0.4985314 * var_xyz[2]
    var_g = -0.9692660 * var_xyz[0] + 1.8760108 * var_xyz[1] + 0.0415560 * var_xyz[2]
    var_b = 0.0556434 * var_xyz[0] - 0.2040259 * var_xyz[1] + 1.0572252 * var_xyz[2]
    var_rgb = [var_r, var_g, var_b]

    var_rgb = [1.055 * (val ** (1 / 2.4)) - 0.055 if val > 0.0031308 else 12.92 * val for val in var_rgb]
    rgb = [val * 255 for val in var_rgb]

    return rgb
