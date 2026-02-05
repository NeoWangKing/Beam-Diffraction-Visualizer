# /BeamType/algorithms/rasterized.py
import numpy as np

def Basic_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 632.8e-9, z: float = 1.0) -> np.ndarray:

    x = np.linspace(-plotrange, plotrange, resolution)
    y = np.linspace(-plotrange, plotrange, resolution)
    X, Y = np.meshgrid(x, y)
    phi = np.angle(X + 1j * Y)
    k = 2 * np.pi / wavelength

    amplitude = z**0
    phase = phi * 0 + k * z

    Beam = amplitude * np.exp(1j * phase)

    return Beam

def Gaussian_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 0.5, z: float = 1.0, w0: float = 1e-2) -> np.ndarray:

    x = np.linspace(-plotrange, plotrange, resolution)
    y = np.linspace(-plotrange, plotrange, resolution)
    X, Y = np.meshgrid(x, y)
    phi = np.angle(X + 1j * Y)

    k = 2 * np.pi / wavelength
    z_R = k * (w0**2) / 2

    if z==0:
        amplitude = np.exp(-(X**2 + Y**2) / w0**2)
        phase = -np.angle(X + 1j * Y) + k * z
    elif z>0:
        R = z_R * ((z / z_R) + (z_R / z))
    
        w = w0 * np.sqrt(1 + (z / z_R)**2)

        amplitude = (w0 / w) * np.exp(-(X**2 + Y**2) / w**2)
        phase = (k * (X**2 + Y**2) / (2 * R) - phi + k * z)
    else:
        raise ValueError("z must be non-negative for Gaussian Beam.")
    
    Beam = amplitude * np.exp(1j * phase)

    return Beam

def Laguerre_Gaussian_Beam_rasterized(plotrange: float = 1e-2, resolution: int = 1024, wavelength: float = 0.5, z: float = 1.0, w0: float = 1e-2, l: int = 1, p: int = 0) -> np.ndarray:
    from scipy.special import genlaguerre
    from scipy.special import factorial as fact

    x = np.linspace(-plotrange, plotrange, resolution)
    y = np.linspace(-plotrange, plotrange, resolution)
    X, Y = np.meshgrid(x, y)
    phi = np.angle(X + 1j * Y)

    k = 2 * np.pi / wavelength
    z_R = k * (w0**2) / 2

    if z>=0:
    
        w = w0 * np.sqrt(1 + (z / z_R)**2)

        A = np.sqrt((2 / np.pi) * (fact(p) / fact(p + np.abs(l)))) / w

        amplitude = A * (np.sqrt(2 * (X**2 + Y**2)) / w)**(np.abs(l)) * genlaguerre(p, np.abs(l))(2 * (X**2 + Y**2) / w**2) * np.exp(-(X**2 + Y**2) / w**2)

        phase = -1 * (k * (X**2 + Y**2) * z / (2 * (z**2 + z_R**2)) - (2 * p + l + 1) * np.arctan(z / z_R) + l * phi)
    else:
        raise ValueError("z must be non-negative for Laguerre-Gaussian Beam.")
    
    Beam = amplitude * np.exp(1j * phase)

    return Beam