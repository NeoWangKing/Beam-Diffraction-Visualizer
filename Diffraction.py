import numpy as np
import matplotlib.pyplot as plt
import Beam as bt
import Aperture as ap
import time

class Diffraction:
    def __init__(self, input_beam: bt.Beam, aperture: ap.Aperture, distance=0.1):
        self.input_beam = input_beam
        self.aperture = aperture
        self.distance = distance
        self.plotrange = input_beam.plotrange
        self.resolution = input_beam.resolution

        if self.input_beam.plotrange[0] != self.aperture.plotrange[0] or self.input_beam.resolution[0] != self.aperture.resolution[0]:
            raise ValueError("Input beam and aperture must have the same plotrange and resolution.")
        
        self.diffracted_field = self.compute_diffraction()

    def compute_diffraction(self):
        print("Computing diffraction using Fresnel approximation...")
        U_0 = self.input_beam.rasterized() * self.aperture.rasterized()
        
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        k = 2 * np.pi / self.input_beam.lam[0]

        fx = np.fft.fftfreq(self.resolution[0], d=(2 * self.plotrange[0]) / self.resolution[0])
        fy = np.fft.fftfreq(self.resolution[0], d=(2 * self.plotrange[0]) / self.resolution[0])
        FX, FY = np.meshgrid(fx, fy)

        H = np.exp(1j * k * self.distance) * np.exp(-1j * (np.pi * self.input_beam.lam[0] * self.distance) * (FX**2 + FY**2))

        U_0_hat = np.fft.fft2(np.fft.fftshift(U_0))
        U_out_hat = U_0_hat * H
        U_out = np.fft.ifftshift(np.fft.ifft2(U_out_hat))

        print("Diffraction computation complete.")
        return U_out

    def plot_diffraction_intensity(self):
        intensity = np.abs(self.diffracted_field)**2

        plt.imshow(intensity, extent=[-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]], cmap='inferno')
        plt.clim(0, np.max(intensity))
        plt.title("Diffracted Beam Intensity")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")

    def plot_diffraction_phase(self):
        phase = np.angle(self.diffracted_field) % (2 * np.pi)

        plt.imshow(phase, extent=[-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]], cmap='gray')
        plt.clim(0, 2 * np.pi)
        plt.title("Diffracted Beam Phase")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
    
    def plot_diffraction(self):
        plt.subplot(1,2,1)
        self.plot_diffraction_intensity()
        plt.subplot(1,2,2)
        self.plot_diffraction_phase()
        pass

def plot_diffraction_test(plotrange=1e-3, resolution=1024, z=0.1, lam=632.8e-9, radius=0.3e-3, distance=1):
    beam = bt.Beam(plotrange=plotrange, resolution=resolution, z=z, lam=lam)

    aperture = ap.Circular_Aperture(plotrange=plotrange, resolution=resolution, radius=radius)

    diffraction = Diffraction(input_beam=beam, aperture=aperture, distance=distance)

    plt.subplot(2, 3, 1)
    beam.plot_intensity()
    plt.subplot(2, 3, 2)
    beam.plot_phase()
    plt.subplot(2, 3, 3)
    aperture.plot_aperture()
    plt.subplot(2, 3, 4)
    diffraction.plot_diffraction_intensity()
    plt.subplot(2, 3, 5)
    diffraction.plot_diffraction_phase()
    plt.subplot(2, 3, 6)
    plt.axis('off')
    plt.suptitle("Beam Diffraction through Circular Aperture")

if __name__ == "__main__":
    plotrange = 2e-3
    resolution = 4096
    z = 0.1
    lam = 632.8e-9
    radius = 1e-3
    distance = 0.5

    plot_diffraction_test(plotrange=plotrange, resolution=resolution, z=z, lam=lam, radius=radius, distance=distance)
    plt.show()