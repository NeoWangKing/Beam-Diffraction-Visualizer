# /beamtype/algorithms/rasterized.py
from numpy import linspace, meshgrid, angle, pi, exp, ndarray, sqrt, arctan

def Plain_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 632.8e-9, z: float = 1.0) -> ndarray:

    x = linspace(-plotrange, plotrange, resolution)
    y = linspace(-plotrange, plotrange, resolution)
    X, Y = meshgrid(x, y)
    phi = angle(X + 1j * Y)
    k = 2 * pi / wavelength

    amplitude = z**0
    phase = phi * 0 + k * z

    Beam = amplitude * exp(1j * phase)

    return Beam

def Gaussian_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 0.5, z: float = 1.0, w0: float = 1e-2) -> ndarray:

    x = linspace(-plotrange, plotrange, resolution)
    y = linspace(-plotrange, plotrange, resolution)
    X, Y = meshgrid(x, y)
    phi = angle(X + 1j * Y)

    k = 2 * pi / wavelength
    z_R = k * (w0**2) / 2

    if z==0:
        amplitude = exp(-(X**2 + Y**2) / w0**2)
        phase = -angle(X + 1j * Y) + k * z
    elif z>0:
        R = z_R * ((z / z_R) + (z_R / z))
    
        w = w0 * sqrt(1 + (z / z_R)**2)

        amplitude = (w0 / w) * exp(-(X**2 + Y**2) / w**2)
        phase = (k * (X**2 + Y**2) / (2 * R) - phi + k * z)
    else:
        raise ValueError("z must be non-negative for Gaussian Beam.")
    
    Beam = amplitude * exp(1j * phase)

    return Beam

def Laguerre_Gaussian_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 0.5, z: float = 1.0, w0: float = 1e-2, l: int = 1, p: int = 0) -> ndarray:
    from scipy.special import genlaguerre
    from scipy.special import factorial as fact

    x = linspace(-plotrange, plotrange, resolution)
    y = linspace(-plotrange, plotrange, resolution)
    X, Y = meshgrid(x, y)
    phi = angle(X + 1j * Y)

    k = 2 * pi / wavelength
    z_R = k * (w0**2) / 2

    if z>=0:
    
        w = w0 * sqrt(1 + (z / z_R)**2)

        A = sqrt((2 / pi) * (fact(p) / fact(p + abs(l)))) / w

        amplitude = A * (sqrt(2 * (X**2 + Y**2)) / w)**(abs(l)) * genlaguerre(p, abs(l))(2 * (X**2 + Y**2) / w**2) * exp(-(X**2 + Y**2) / w**2)

        phase = -1 * (k * (X**2 + Y**2) * z / (2 * (z**2 + z_R**2)) - (2 * p + l + 1) * arctan(z / z_R) + l * phi)
    else:
        raise ValueError("z must be non-negative for Laguerre-Gaussian Beam.")
    
    Beam = amplitude * exp(1j * phase)

    return Beam