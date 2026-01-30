import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.special import genlaguerre

def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)

#create a basic Beam class
class Beam:
    def __init__(self, range=1e-3, resolution=1024, z=0., lam=632.8e-9):
        self.range = range
        self.resolution = resolution
        self.z = z
        self.lam = lam
        pass

    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        phase = 0 * X * Y

        Beam = (self.z**0) * np.exp(1j * phase)

        return Beam
    
    def plot_intensity(self):
        self.Beam = self.rasterized_Beam()
        self.intensity = np.abs(self.Beam)**2
        mpltensity = np.max(self.intensity)

        plt.imshow(self.intensity / mpltensity, extent=(-self.range, self.range, -self.range, self.range), cmap='inferno')

        plt.colorbar(label='Intensity', ticks=[0, 0.25, 0.5, 0.75, 1])
        plt.clim(0, 1)
        plt.title('Beam Intensity Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

    def plot_phase(self):
        self.phase = np.angle(self.rasterized_Beam())%(2 * np.pi)

        plt.imshow(self.phase, extent=(-self.range, self.range, -self.range, self.range), cmap='gray')

        plt.colorbar(label='Phase')
        plt.clim(0, (2 * np.pi))
        plt.title('Beam Phase Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

#create the Gaussian_Beam class
class Gaussian_Beam(Beam):
    def __init__(self, range=1e-3, resolution=1024, z=0., lam=632.8e-9, w0=1e-3):
        super().__init__(range, resolution, z, lam)

        self.w0 = w0
        
        self.Beam = self.rasterized_Beam()
        pass
    
    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)
        self.phi = np.angle(X + 1j * Y)
        self.k = 2 * np.pi / self.lam
        self.z_R = self.k * (self.w0**2) / 2

        if self.z==0:
            phase = (self.k * self.z - self.phi) * (X / X)

            Beam = np.exp(-(X**2 + Y**2) / self.w0**2) * np.exp(1j * phase)
        elif self.z>0:
            self.R = self.z_R * ((self.z / self.z_R) + (self.z_R / self.z))
        
            self.w = self.w0 * np.sqrt(1 + (self.z / self.z_R)**2)

            phase = (self.k * (X**2 + Y**2) / (2 * self.R) - self.phi + self.k * self.z)

            Beam = (self.w0 / self.w) * np.exp(-(X**2 + Y**2) / self.w**2) * np.exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0) * np.exp(1j * phase)

        return Beam

class Laguerre_Gaussian_Beam(Beam):
    def __init__(self, range=0.001, resolution=1024, z=0, lam=6.328e-7, l=1, p=0, w0=1e-3):
        super().__init__(range, resolution, z, lam)

        self.l = l
        self.p = p
        self.w0 = w0
        
        self.Beam = self.rasterized_Beam()
        pass

    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)
        self.phi = np.angle(X + 1j * Y)
        self.k = 2 * np.pi / self.lam
        self.z_R = self.k * (self.w0**2) / 2

        if self.z>=0:
        
            self.w = self.w0 * np.sqrt(1 + (self.z / self.z_R)**2)

            self.A = np.sqrt((2 / np.pi) * (fact(self.p) / fact(self.p + np.abs(self.l)))) / self.w

            phase = -1 * (self.k * (X**2 + Y**2) * self.z / (2 * (self.z**2 + self.z_R**2)) - (2 * self.p + self.l + 1) * np.arctan(self.z / self.z_R) + self.l * self.phi)

            Beam = self.A * (np.sqrt(2 * (X**2 + Y**2)) / self.w)**(np.abs(self.l)) * genlaguerre(self.p, np.abs(self.l))(2 * (X**2 + Y**2) / self.w**2) * np.exp(-(X**2 + Y**2) / self.w**2) * np.exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0) * np.exp(1j * phase)

        return Beam

def show_beam_examples():
    line = 2
    column = 3

    num = 1
    range = 2e-3
    resolution = 1024
    lam=632.8e-9
    z=0.
    beam = Beam(range=range, resolution=resolution, z=z, lam=lam)
    beam.rasterized_Beam()
    plt.subplot(line, column, num)
    beam.plot_intensity()
    plt.subplot(line, column, num + column)
    beam.plot_phase()
    
    num = 2
    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    gaussian_beam = Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam)
    gaussian_beam.rasterized_Beam()
    plt.subplot(line, column, num)
    gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    gaussian_beam.plot_phase()

    num = 3
    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    l = 3
    p = 0
    laguerre_gaussian_beam = Laguerre_Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam, l=l, p=p)
    laguerre_gaussian_beam.rasterized_Beam()
    plt.subplot(line, column, num)
    laguerre_gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    laguerre_gaussian_beam.plot_phase()

    plt.show()
    pass

if __name__ == "__main__":
    show_beam_examples()