import numpy as np
import matplotlib.pyplot as plt
import beamtype as bt

def run():
    display = True
    details = True

    plotrange = "1e-2"
    resolution = "1024"
    wavelength = "632.8e-9"
    z = "1.0"

    beam = bt.PBeam(plotrange=plotrange, resolution=resolution, wavelength=wavelength, z=z)
    beam.plot_intensity(disp=display, deta=details)
    beam.plot_phase(disp=display, deta=details)

    plotrange = "1e-2"
    resolution = "1024"
    wavelength = "632.8e-9"
    z = "10"
    w0 = "1e-2"
    beam = bt.GBeam(plotrange=plotrange, resolution=resolution, wavelength=wavelength, z=z, w0=w0)
    beam.plot_intensity(disp=display, deta=details)
    beam.plot_phase(disp=display, deta=details)

    plotrange = "1e-2"
    resolution = "1024"
    wavelength = "632.8e-9"
    z = "10"
    w0 = "1e-2"
    l = "5"
    p = "1"
    beam = bt.LGBeam(plotrange=plotrange, resolution=resolution, wavelength=wavelength, z=z, w0=w0, l=l, p=p)
    beam.plot_intensity(disp=display, deta=details)
    beam.plot_phase(disp=display, deta=details)
    pass

if __name__ == "__main__":
    run()