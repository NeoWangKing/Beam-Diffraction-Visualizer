import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.special import genlaguerre

def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)

def get_beam_list():
    return ["basic", "gaussian", "laguerre-gaussian"]

#create a basic Beam class
class Beam:
    def __init__(self, range=1e-3, resolution=1024, z=0., lam=632.8e-9):
        self.beamtype = "Basic Beam"
        self.range = range
        self.resolution = resolution
        self.z = z
        self.lam = lam
        pass

    def list(self):
        print(self.beamtype, ":")
        for name, value in self.__dict__.items():
            if name != "beamtype":
                print(f"self.{name} = {value}")
            else:
                pass
        print("")

    def get_var(self):
        for name in self.__dict__:
            if name != "beamtype" and name != "lam":
                self.__dict__[name] = eval(input(f"Enter value for {name} (current value: {self.__dict__[name]}): "))
            elif name == "lam":
                self.__dict__[name] = eval(input(f"Enter value for lam(nm) (current value: {self.__dict__[name] * 1e9} nm): ")) * 1e-9
            else:
                pass
        print("Variables updated.\n")


    def rasterized_Beam(self):
        x = np.linspace(-self.range, self.range, self.resolution)
        y = np.linspace(-self.range, self.range, self.resolution)
        X, Y = np.meshgrid(x, y)

        phase = 0 * X * Y

        Beam = (self.z**0) * np.exp(1j * phase)

        return Beam
    
    def plot_intensity(self):
        self.intensity = np.abs(self.rasterized_Beam())**2
        mpltensity = np.max(self.intensity)

        plt.imshow(self.intensity / mpltensity, extent=(-self.range, self.range, -self.range, self.range), cmap='inferno')

        #plt.colorbar(label='Intensity')
        plt.clim(0, 1)
        plt.title('Beam Intensity Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

    def plot_phase(self):
        self.phase = np.angle(self.rasterized_Beam())%(2 * np.pi)

        plt.imshow(self.phase, extent=(-self.range, self.range, -self.range, self.range), cmap='gray')

        #plt.colorbar(label='Phase')
        plt.clim(0, (2 * np.pi))
        plt.title('Beam Phase Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
    
    def show_beam_examples(self):
        plt.subplot(1,2,1)
        self.plot_intensity()
        plt.subplot(1,2,2)
        self.plot_phase()
        plt.show()
        pass

#create the Gaussian_Beam class
class Gaussian_Beam(Beam):
    def __init__(self, range=1e-3, resolution=1024, z=0., lam=632.8e-9, w0=1e-3):
        super().__init__(range, resolution, z, lam)
        self.beamtype = "Gaussian Beam"
        self.w0 = w0
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
        self.beamtype = "Laguerre-Gaussian Beam"
        self.w0 = w0
        self.l = l
        self.p = p
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

def show_beam_test(range=2e-3, resolution=1024, lam=632.8e-9, z=0., w0=1e-3, l = 1, p = 0):
    line = 2
    column = 3

    num = 1
    beam = Beam(range=range, resolution=resolution, z=z, lam=lam)
    beam.list()
    plt.subplot(line, column, num)
    beam.plot_intensity()
    plt.subplot(line, column, num + column)
    beam.plot_phase()
    
    num = 2
    gaussian_beam = Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam)
    gaussian_beam.list()
    plt.subplot(line, column, num)
    gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    gaussian_beam.plot_phase()

    num = 3
    laguerre_gaussian_beam = Laguerre_Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam, l=l, p=p)
    laguerre_gaussian_beam.list()
    plt.subplot(line, column, num)
    laguerre_gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    laguerre_gaussian_beam.plot_phase()

    plt.show()
    pass

if __name__ == "__main__":
    range = 2e-3
    resolution = 1024
    lam=632.8e-9
    z=1
    w0=1e-3
    l = 1
    p = 0
    show_beam_test(range=range, resolution=resolution, lam=lam, z=z, w0=w0, l=l, p=p)