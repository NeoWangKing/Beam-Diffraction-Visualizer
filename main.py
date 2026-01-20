import numpy as np
import matplotlib.pyplot as plt

#create a basic Beam class
class Beam:
    def __init__(self, range=1e-3, resolution=1024):
        self.range = range
        self.resolution = resolution
        pass

    def rasterized_Beam(self, z=0., phi=0.):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        Beam = ((X + 1j * Y) / (X + 1j * Y)) * (z**0)

        return Beam
    
    def plot_intensity(self, z=0., phi=0.):
        self.intensity = np.abs(self.rasterized_Beam(z=z, phi=phi))**2

        plt.imshow(self.intensity, extent=(-self.range, self.range, -self.range, self.range), cmap='inferno')
        plt.colorbar(label='Intensity', extend='max')
        plt.title('Beam Intensity Distribution (l={self.l}, p={self.p})')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

        plt.show()

    def plot_phase(self, z=0., phi=0.):
        self.angle = np.angle(self.rasterized_Beam(z=z,phi=phi))%(2 * np.pi)

        plt.imshow(self.angle, extent=(-self.range, self.range, -self.range, self.range), cmap='gray')
        plt.colorbar(label='Phase')
        plt.clim(0, 2 * np.pi)
        plt.title('LG Beam Phase Distribution (l={self.l}, p={self.p})')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        
        plt.show()

#create the G_Beam class
class G_Beam(Beam):
    def __init__(self, range=1e-3, resolution=1024, w0=1e-3, lam=632.8e-9):
        super().__init__(range, resolution)

        self.w0 = w0
        self.lam = lam
        self.k = 2 * np.pi / self.lam
        self.z_R = self.k * (self.w0**2) / 2
        
        self.Beam = self.rasterized_Beam()
        pass
    
    def rasterized_Beam(self, z=0., phi=0.):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        if z==0:
            Beam = np.exp(-(X**2 + Y**2) / self.w0**2) * np.exp(1j*(self.k * z - phi))
        elif z>0:
            R = self.z_R * ((z / self.z_R) + (self.z_R / z))
        
            w = self.w0 * np.sqrt(1 + (z / self.z_R)**2)

            Beam = (self.w0 / w) * np.exp(-(X**2 + Y**2) / w**2) * np.exp(1j * (self.k * (X**2 + Y**2) / (2 * R) - phi + self.k * z))
        else:
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (z**0)

        return Beam

    

if __name__ == "__main__":
    range = 1e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    phi=0.
    Beam = G_Beam(range=range, resolution=resolution, w0=w0, lam=lam)
    Beam.rasterized_Beam(z=z, phi=phi)
    Beam.plot_intensity(z=z, phi=phi)
    Beam.plot_phase(z=z, phi=phi)
    pass