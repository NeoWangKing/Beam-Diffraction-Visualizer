import BeamType as bt

if __name__ == "__main__":
    range = 2e-3
    resolution = 1024
    lam=632.8e-9
    z=0.
    Beam = bt.Beam(range=range, resolution=resolution, z=z, lam=lam)
    Beam.rasterized_Beam()
    Beam.plot_intensity()
    Beam.plot_phase()
    
    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    Gaussian_Beam = bt.Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam)
    Gaussian_Beam.rasterized_Beam()
    Gaussian_Beam.plot_intensity()
    Gaussian_Beam.plot_phase()

    range = 2e-3
    resolution = 1024
    w0=1e-3
    lam=632.8e-9
    z=0.
    l = 3
    p = 0
    Laguerre_Gaussian_Beam = bt.Laguerre_Gaussian_Beam(range=range, resolution=resolution, z=z, w0=w0, lam=lam, l=l, p=p)
    Laguerre_Gaussian_Beam.rasterized_Beam()
    Laguerre_Gaussian_Beam.plot_intensity()
    Laguerre_Gaussian_Beam.plot_phase()
    pass