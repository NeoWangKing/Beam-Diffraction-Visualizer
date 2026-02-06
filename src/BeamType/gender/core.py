# /beamtype/gender/core.py

from numpy import abs, max, ndarray, angle, pi
from matplotlib.pyplot import imshow, colorbar, clim, title, xlabel, ylabel, show

def gender_intensity(beam_ras: ndarray, disp: bool = False, deta: bool = False):
    intensity = abs(beam_ras)**2
    maxintensity = max(intensity)
    imshow(intensity / maxintensity, cmap='inferno')
    if deta:
        colorbar(label='Intensity')
        clim(0, 1)
        title(f'Intensity Distribution')
        xlabel('x (m)')
        ylabel('y (m)')
    if disp:
        show()


def gender_phase(beam_ras: ndarray, disp: bool = False, deta: bool = False):
    phase = angle(beam_ras) % (2 * pi)
    imshow(phase, cmap='gray')
    if deta:
        colorbar(label='Phase')
        clim(0, (2 * pi))
        title(f'Phase Distribution')
        xlabel('x (m)')
        ylabel('y (m)')
    if disp:
        show()