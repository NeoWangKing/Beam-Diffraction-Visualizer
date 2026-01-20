import numpy as np
import matplotlib.pyplot as plt

#create a basic Beam class
class Beam:
    def __init__(self, range=1e-3, resolution=1024, z=0., phi=0.):
        self.range = range
        self.resolution = resolution
        self.z = z
        self.phi = phi
        pass

    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0)

        return Beam
    
    def plot_intensity(self):
        self.intensity = np.abs(self.rasterized_Beam())**2

        plt.imshow(self.intensity, extent=(-self.range, self.range, -self.range, self.range), cmap='inferno')
        plt.colorbar(label='Intensity', extend='max')
        plt.title('Beam Intensity Distribution (l={self.l}, p={self.p})')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

        plt.show()

    def plot_phase(self):
        self.angle = np.angle(self.rasterized_Beam())%(2 * np.pi)

        plt.imshow(self.angle, extent=(-self.range, self.range, -self.range, self.range), cmap='gray')
        plt.colorbar(label='Phase')
        plt.clim(0, 2 * np.pi)
        plt.title('LG Beam Phase Distribution (l={self.l}, p={self.p})')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        
        plt.show()

#create the G_Beam class
class G_Beam(Beam):
    def __init__(self, range=1e-3, resolution=1024, z=0., phi=0., w0=1e-3, lam=632.8e-9):
        super().__init__(range, resolution, z, phi)

        self.w0 = w0
        self.lam = lam
        self.k = 2 * np.pi / self.lam
        self.z_R = self.k * (self.w0**2) / 2
        
        self.Beam = self.rasterized_Beam()
        pass
    
    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        if z==0:
            Beam = np.exp(-(X**2 + Y**2) / self.w0**2) * np.exp(1j*(self.k * self.z - phi))
        elif z>0:
            R = self.z_R * ((self.z / self.z_R) + (self.z_R / self.z))
        
            w = self.w0 * np.sqrt(1 + (self.z / self.z_R)**2)

            Beam = (self.w0 / w) * np.exp(-(X**2 + Y**2) / w**2) * np.exp(1j * (self.k * (X**2 + Y**2) / (2 * R) - phi + self.k * self.z))
        else:
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z**0)

        return Beam

    

if __name__ == "__main__":
    range = 1e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    phi=0.
    Beam = G_Beam(range=range, resolution=resolution, z=z, phi=phi, w0=w0, lam=lam)
    Beam.rasterized_Beam()
    Beam.plot_intensity()
    Beam.plot_phase()
    pass