import numpy as np
from numpy import exp
import matplotlib.pyplot as plt
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

        Beam = (self.z**0) * exp(1j * phase)

        return Beam
    
    def plot_intensity(self):
        self.Beam = self.rasterized_Beam()
        self.intensity = np.abs(self.Beam)**2

        plt.imshow(self.intensity, extent=(-self.range, self.range, -self.range, self.range), cmap='inferno')
        plt.colorbar(label='Intensity', extend='max')
        plt.title('Beam Intensity Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

        plt.show()

    def plot_phase(self):
        self.phase = np.angle(self.rasterized_Beam())%(2 * np.pi)

        plt.imshow(self.phase, extent=(-self.range, self.range, -self.range, self.range), cmap='gray')
        plt.colorbar(label='Phase')
        plt.clim(0, 2 * np.pi)
        plt.title('LG Beam Phase Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        
        plt.show()

#create the G_Beam class
class G_Beam(Beam):
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

            Beam = exp(-(X**2 + Y**2) / self.w0**2) * exp(1j * phase)
        elif self.z>0:
            self.R = self.z_R * ((self.z / self.z_R) + (self.z_R / self.z))
        
            self.w = self.w0 * np.sqrt(1 + (self.z / self.z_R)**2)

            phase = (self.k * (X**2 + Y**2) / (2 * self.R) - self.phi + self.k * self.z)

            Beam = (self.w0 / self.w) * exp(-(X**2 + Y**2) / self.w**2) * exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0) * exp(1j * phase)

        return Beam

class LG_Beam(Beam):
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

            Beam = self.A * (np.sqrt(2 * (X**2 + Y**2)) / self.w)**(np.abs(self.l)) * genlaguerre(self.p, np.abs(self.l))(2 * (X**2 + Y**2) / self.w**2) * exp(-(X**2 + Y**2) / self.w**2) * exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0) * exp(1j * phase)

        return Beam
        
    

if __name__ == "__main__":
    range = 2e-3
    resolution = 1024
    lam=632.8e-9
    z=0.
    Beam = Beam(range=range, resolution=resolution, z=z, lam=lam)
    Beam.rasterized_Beam()
    Beam.plot_intensity()
    Beam.plot_phase()
    
    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    G_Beam = G_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam)
    G_Beam.rasterized_Beam()
    G_Beam.plot_intensity()
    G_Beam.plot_phase()

    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    l = 3
    p = 0
    LG_Beam = LG_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam, l=l, p=p)
    LG_Beam.rasterized_Beam()
    LG_Beam.plot_intensity()
    LG_Beam.plot_phase()
    pass