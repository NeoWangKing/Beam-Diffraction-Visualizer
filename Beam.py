import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre

def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)

def get_beam_list():
    return ["basic", "gaussian", "laguerre-gaussian"]

def var_key():
    return{"Value":0, "Parameter":1, "Unit":2}

#create a basic Beam class
class Beam:
    def __init__(self, plotrange=1e-3, resolution=1024, z=0., lam=632.8e-9):
        self.beamtype = ["Basic Beam", "Beam Type", ""]
        self.plotrange = [plotrange, "Render plotRange", "m"]
        self.resolution = [resolution, "Resolution", "pixels"]
        self.z = [z, "Propagation Distance", "m"]
        self.lam = [lam, "Wavelength", "nm"]
        pass
    
    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        phase = 0 * X * Y

        Beam = (self.z[0]**0) * np.exp(1j * phase)

        return Beam

    def list(self):
        print(self.beamtype[0], ":")
        print(f"{'Parameter':<25}{'Variable':<15}{'Value':<10}{'Unit'}")
        for name, value in self.__dict__.items():
            if name != "beamtype" and name != "lam":
                print(f"{value[1]:<25}{'(.'+name+'): ':<15}{value[0]:<10}{value[2]}")
            elif name == "lam":
                print(f"{value[1]:<25}{'(.'+name+'): ':<15}{value[0]*1e9:<10}nm")
            else:
                pass
        print("")

    def get_var(self):
        for name in self.__dict__:
            if name != "beamtype" and name != "lam":
                self.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {self.__dict__[name][0]}): "))
            elif name == "lam":
                self.__dict__[name][0] = eval(input(f"Enter value for lam(nm) (current value: {self.__dict__[name][0] * 1e9} nm): ")) * 1e-9
            else:
                pass
        print("Variables updated.\n")
    
    def plot_intensity(self):
        self.intensity = np.abs(self.rasterized())**2
        mpltensity = np.max(self.intensity)

        plt.imshow(self.intensity / mpltensity, extent=(-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]), cmap='inferno')

        #plt.colorbar(label='Intensity')
        plt.clim(0, 1)
        plt.title(f'{self.beamtype[0]} Intensity Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')

    def plot_phase(self):
        self.phase = np.angle(self.rasterized())%(2 * np.pi)

        plt.imshow(self.phase, extent=(-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]), cmap='gray')

        #plt.colorbar(label='Phase')
        plt.clim(0, (2 * np.pi))
        plt.title(f'{self.beamtype[0]} Phase Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
    
    def plot_beam(self):
        plt.subplot(1,2,1)
        self.plot_intensity()
        plt.subplot(1,2,2)
        self.plot_phase()
        pass

#create the Gaussian_Beam class
class Gaussian_Beam(Beam):
    def __init__(self, plotrange=1e-3, resolution=1024, z=0., lam=632.8e-9, w0=1e-3):
        super().__init__(plotrange, resolution, z, lam)
        self.beamtype = ["Gaussian Beam", "Beam Type", ""]
        self.w0 = [w0, "Beam Waist", "m"]
        pass
    
    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)
        self.phi = np.angle(X + 1j * Y)
        self.k = 2 * np.pi / self.lam[0]
        self.z_R = self.k * (self.w0[0]**2) / 2

        if self.z[0]==0:
            phase = (self.k * self.z[0] - self.phi) * (X / X)
            Beam = np.exp(-(X**2 + Y**2) / self.w0[0]**2) * np.exp(1j * phase)
        elif self.z[0]>0:
            self.R = self.z_R * ((self.z[0] / self.z_R) + (self.z_R / self.z[0]))
        
            self.w = self.w0[0] * np.sqrt(1 + (self.z[0] / self.z_R)**2)

            phase = (self.k * (X**2 + Y**2) / (2 * self.R) - self.phi + self.k * self.z[0])

            Beam = (self.w0[0] / self.w) * np.exp(-(X**2 + Y**2) / self.w**2) * np.exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z[0]**0) * np.exp(1j * phase)
        return Beam

class Laguerre_Gaussian_Beam(Beam):
    def __init__(self, plotrange=0.001, resolution=1024, z=0, lam=6.328e-7, l=1, p=0, w0=1e-3):
        super().__init__(plotrange, resolution, z, lam)
        self.beamtype = ["Laguerre-Gaussian Beam", "Beam Type", ""]
        self.w0 = [w0, "Beam Waist", "m"]
        self.l = [l, "Azimuthal Index", ""]
        self.p = [p, "Radial Index", ""]
        pass

    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)
        self.phi = np.angle(X + 1j * Y)
        self.k = 2 * np.pi / self.lam[0]
        self.z_R = self.k * (self.w0[0]**2) / 2

        if self.z[0]>=0:
        
            self.w = self.w0[0] * np.sqrt(1 + (self.z[0] / self.z_R)**2)

            self.A = np.sqrt((2 / np.pi) * (fact(self.p[0]) / fact(self.p[0] + np.abs(self.l[0])))) / self.w

            phase = -1 * (self.k * (X**2 + Y**2) * self.z[0] / (2 * (self.z[0]**2 + self.z_R**2)) - (2 * self.p[0] + self.l[0] + 1) * np.arctan(self.z[0] / self.z_R) + self.l[0] * self.phi)

            Beam = self.A * (np.sqrt(2 * (X**2 + Y**2)) / self.w)**(np.abs(self.l[0])) * genlaguerre(self.p[0], np.abs(self.l[0]))(2 * (X**2 + Y**2) / self.w**2) * np.exp(-(X**2 + Y**2) / self.w**2) * np.exp(1j * phase)
        else:
            phase = 0
            Beam = ((X + 1j * Y) / (X + 1j * Y)) * (self.z[0]**0) * np.exp(1j * phase)

        return Beam

def show_beam_test(plotrange=2e-3, resolution=1024, lam=632.8e-9, z=0., w0=1e-3, l = 1, p = 0):
    line = 2
    column = 3

    num = 1
    beam = Beam(plotrange=plotrange, resolution=resolution, z=z, lam=lam)
    beam.list()
    plt.subplot(line, column, num)
    beam.plot_intensity()
    plt.subplot(line, column, num + column)
    beam.plot_phase()
    
    num += 1
    gaussian_beam = Gaussian_Beam(plotrange=plotrange, resolution=resolution, z=z, w0=w0, lam=lam)
    gaussian_beam.list()
    plt.subplot(line, column, num)
    gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    gaussian_beam.plot_phase()

    num += 1
    laguerre_gaussian_beam = Laguerre_Gaussian_Beam(plotrange=plotrange, resolution=resolution, z=z, w0=w0, lam=lam, l=l, p=p)
    laguerre_gaussian_beam.list()
    plt.subplot(line, column, num)
    laguerre_gaussian_beam.plot_intensity()
    plt.subplot(line, column, num + column)
    laguerre_gaussian_beam.plot_phase()

    plt.show()
    pass

if __name__ == "__main__":
    plotrange = 2e-3
    resolution = 1024
    lam=632.8e-9
    z=1
    w0=1e-3
    l = 3
    p = 1
    show_beam_test(plotrange=plotrange, resolution=resolution, lam=lam, z=z, w0=w0, l=l, p=p)