import numpy as np
import matplotlib.pyplot as plt

class Aperture:
    def __init__(self, plotrange=1e-3, resolution=1024):
        self.aperturetype = ["Generic Aperture", "Aperture Type", ""]
        self.plotrange = [plotrange, "Render plotRange", "m"]
        self.resolution = [resolution, "Resolution", "pixels"]
    
    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        aperture = (np.ones_like(X) + np.ones_like(Y)) / 2

        return aperture
    
    def list(self):
        print(self.aperturetype[0], ":")
        print(f"{'Parameter':<25}{'Variable':<15}{'Value':<10}{'Unit'}")
        for name, value in self.__dict__.items():
            if name != "aperturetype":
                print(f"{value[1]:<25}{'(.'+name+'): ':<15}{value[0]:<10}{value[2]}")
            else:
                pass
        print("")

    def get_var(self):
        for name in self.__dict__:
            if name != "aperturetype":
                self.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {self.__dict__[name][0]} {self.__dict__[name][2]}): "))
            else:
                pass
        print("Variables updated.\n")

    def plot_aperture(self):
        aperture = self.rasterized()
        plt.imshow(aperture, extent=[-self.plotrange[0], self.plotrange[0], -self.plotrange[0], self.plotrange[0]], cmap='gray')
        plt.clim(0, 1)
        plt.title(f"{self.aperturetype[0]} Aperture")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")

class Circular_Aperture(Aperture):
    def __init__(self, plotrange=1e-3, resolution=1024, radius=0.5e-3):
        super().__init__(plotrange, resolution)
        self.aperturetype = ["Circular Aperture", "Aperture Type", ""]
        self.radius = [radius, "Radius", "m"]

    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        R = np.sqrt(X**2 + Y**2)

        aperture = np.where(R <= self.radius[0], 1, 0)
        return aperture
    
class Rectangular_Aperture(Aperture):
    def __init__(self, plotrange=1e-3, resolution=1024, width=0.5e-3, height=0.5e-3):
        super().__init__(plotrange, resolution)
        self.aperturetype = ["Rectangular Aperture", "Aperture Type", ""]
        self.width = [width, "Width", "m"]
        self.height = [height, "Height", "m"]

    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        aperture = np.where((np.abs(X) <= self.width[0] / 2) & (np.abs(Y) <= self.height[0] / 2), 1, 0)
        return aperture
    
class Fresnel_half_wave_zone(Aperture):
    def __init__(self, plotrange=1e-3, resolution=1024, half_lam_radius=0.3e-3, n_zones=10, type=0):
        super().__init__(plotrange, resolution)
        self.aperturetype = ["Fresnel Half-Wave Zone Aperture", "Aperture Type", ""]
        self.half_lam_radius = [half_lam_radius, "Half Wavelength Radius", "m"]
        self.n_zones = [n_zones, "Number of Zones", ""]
        self.type = [type, "Aperture Type (0: type-0, 1: type-1)", ""]

    def rasterized(self):
        x = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        y = np.linspace(-self.plotrange[0], self.plotrange[0], self.resolution[0])
        X, Y = np.meshgrid(x, y)

        R = np.sqrt(X**2 + Y**2)
        aperture = np.zeros_like(R)

        if n_zones >= 0:
            for n in range(0, int(self.n_zones[0])):
                r_inner = np.sqrt(n) * self.half_lam_radius[0]
                r_outer = np.sqrt(n + 1) * self.half_lam_radius[0]
                aperture += np.where((R >= r_inner) & (R < r_outer), (n + 1 + self.type[0]) % 2, 0)
                if r_inner > (self.plotrange[0] * np.sqrt(2)):
                    break
        else:
            n = 0
            while np.sqrt(n) * self.half_lam_radius[0] < (self.plotrange[0] * np.sqrt(2)):
                r_inner = np.sqrt(n) * self.half_lam_radius[0]
                r_outer = np.sqrt(n + 1) * self.half_lam_radius[0]
                aperture += np.where((R >= r_inner) & (R < r_outer), (n + 1 + self.type[0]) % 2, 0)
                n += 1

        return aperture

def show_aperture_test(plotrange=1e-3, resolution=1024, radius=0.5e-3, width=0.5e-3, height=0.5e-3, half_lam_radius=0.3e-3, n_zones=10, type=0):
    line = 2
    column = 2

    num = 1
    plotrange = plotrange
    resolution = resolution
    aperture = Aperture(plotrange=plotrange, resolution=resolution)
    aperture.list()
    plt.subplot(line, column, num)
    aperture.plot_aperture()

    num += 1
    radius = radius
    aperture = Circular_Aperture(plotrange=plotrange, resolution=resolution, radius=radius)
    aperture.list()
    plt.subplot(line, column, num)
    aperture.plot_aperture()

    num += 1
    width = width
    height = height
    aperture = Rectangular_Aperture(plotrange=plotrange, resolution=resolution, width=width, height=height)
    aperture.list()
    plt.subplot(line, column, num)
    aperture.plot_aperture()

    num += 1
    half_lam_radius = half_lam_radius
    n_zones = n_zones
    type = type
    aperture = Fresnel_half_wave_zone(plotrange=plotrange, resolution=resolution, half_lam_radius=half_lam_radius, n_zones=n_zones, type=type)
    aperture.list()
    plt.subplot(line, column, num)
    aperture.plot_aperture()

    plt.show()
    pass

if __name__ == "__main__":
    plotrange = 1e-3
    resolution = 1024
    radius = 0.5e-3
    width = 0.5e-3
    height = 0.5e-3
    half_lam_radius = 0.3e-3
    n_zones = 10
    type = 0
    show_aperture_test(plotrange=plotrange, resolution=resolution,radius=radius, width=width, height=height, half_lam_radius=half_lam_radius, n_zones=n_zones, type=type)