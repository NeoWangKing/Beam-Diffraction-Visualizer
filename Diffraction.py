import numpy as np
import matplotlib.pyplot as plt
import BeamType as bt
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

    def compute_diffraction(self):

        '''U_0 = self.input_beam.rasterized() * self.aperture.rasterized()
        k = 2 * np.pi / self.input_beam.lam[0]
        
        fx = np.fft.fftfreq(self.resolution[0], d=(2 * self.plotrange[0]) / self.resolution[0])
        fy = np.fft.fftfreq(self.resolution[0], d=(2 * self.plotrange[0]) / self.resolution[0])
        FX, FY = np.meshgrid(fx, fy)

        H = np.exp(1j * k * self.distance) * np.exp(-1j * (np.pi * self.input_beam.lam[0] * self.distance) * (FX**2 + FY**2))

        U_0_hat = np.fft.fft2(np.fft.fftshift(U_0))

        U_out_hat = U_0_hat * H

        U_out = np.fft.ifftshift(np.fft.ifft2(U_out_hat))'''
        
        U_0 = self.input_beam.rasterized() * self.aperture.rasterized()
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        k = 2 * np.pi / self.input_beam.lam[0]

        U_out = np.zeros_like(U_0, dtype=complex)
        begin = time.perf_counter()
        for i in range(self.resolution[0]):
            for j in range(self.resolution[0]):
                r_ij = np.sqrt((X - X[i, j])**2 + (Y - Y[i, j])**2 + self.distance**2)
                U_out[i, j] = np.sum(U_0 * (np.exp(1j * k * r_ij) / r_ij)) * ( (2 * self.plotrange[0]) / self.resolution[0])**2
                progress = (i * self.resolution[0] + j + 1)
                current = time.perf_counter()
                remaining_time = ((current - begin) / progress * (self.resolution[0]**2 - progress))
                
                print(f"\rComputing Progress: {(progress / (self.resolution[0]**2) * 100):.2f}%({progress}/{self.resolution[0]**2}), Average: {(current - begin) / progress:.4f}s, Estimated: {int(remaining_time / 3600):.0f}h{int(remaining_time / 60 % 60):.0f}m{remaining_time % 60:.0f}s", end="")
        
        print("\nDiffraction computation complete.")
        return U_out

    def plot_diffraction_intensity(self):
        diffracted_field = self.compute_diffraction()
        intensity = np.abs(diffracted_field)**2

        plt.imshow(intensity, extent=[-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]], cmap='inferno')
        plt.clim(0, np.max(intensity))
        plt.title("Diffracted Beam Intensity")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")

    def plot_diffraction_phase(self):
        diffracted_field = self.compute_diffraction()
        phase = np.angle(diffracted_field) % (2 * np.pi)

        plt.imshow(phase, extent=[-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]], cmap='gray')
        plt.clim(0, 2 * np.pi)
        plt.title("Diffracted Beam Phase")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")

def plot_diffraction_test(plotrange=1e-3, resolution=1024, z=0.1, lam=632.8e-9, l=1, p=0, w0=0.5e-3, radius=0.3e-3, distance=1):
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
    plotrange = 1e-3
    resolution = 1024
    z = 0.1
    lam = 632.8e-9
    w0 = 0.5e-3
    radius = 0.05e-3
    distance = 0.1
    l = 3
    p = 1

    plot_diffraction_test(plotrange=plotrange, resolution=resolution, z=z, lam=lam, w0=w0, radius=radius, distance=distance, l=l, p=p)
    plt.show()