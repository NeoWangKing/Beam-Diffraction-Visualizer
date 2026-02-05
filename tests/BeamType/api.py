# /BeamType/api.py

#导入内部工具模块
from .utils import log_info, log_warning, log_error, validate_input, validate_non_negative
#导入算法模块
from .algorithms import BBeam_ras, GBeam_ras, LGBeam_ras

def parameter(
        para: str,
        value,
        unit: str = None,
        conv: float = 1.0
        ) ->dict:
    '''define a parameter dictionary'''
    return {
        "para": para,
        "value": value,
        "unit": unit,
        "conv": conv
        }

class Beam():

    def __init__(
            self,
            plotrange: float = 1e-2,
            resolution: int = 1024,
            wavelength: float = 632.8e-9,
            z: float = 1.0
            ):
        self.beam_type = parameter(
            para="Beam Type",
            value="Basic",
            unit=None
            )
        self.plotrange = parameter(
            para="Plot Range",
            value=plotrange,
            unit="m"
            )
        self.resolution = parameter(
            para="Resolution",
            value=resolution,
            unit="px"
            )
        self.wavelength = parameter(
            para="Wavelength",
            value=wavelength,
            unit="nm",
            conv=1e9
            )
        self.z = parameter(
            para="Propagation Distance",
            value=z,
            unit="m"
            )
        validate_non_negative(self.plotrange["value"])
        validate_non_negative(self.resolution["value"])
        validate_non_negative(self.wavelength["value"])
        validate_non_negative(self.z["value"])

    def ras(self):
        log_info("Generating Basic Beam Rasterized Field...")
        temp = BBeam_ras(
            plotrange=self.plotrange["value"],
            resolution=self.resolution["value"],
            wavelength=self.wavelength["value"],
            z=self.z["value"]
            )
        log_info("Basic Beam Rasterized Field Generated.")
        return temp
    
    def get_paras(self) -> dict:
        return self.__dict__

class Gaussian_Beam(Beam):

    def __init__(
            self,
            w0: float = 1e-3,
            **kwargs
            ):
        super().__init__(**kwargs)
        self.beam_type["value"] = "Gaussian"
        self.w0 = parameter(
            para="Beam Waist",
            value=w0,
            unit="mm",
            conv=1e3
            )
        validate_non_negative(self.plotrange["value"])
        validate_non_negative(self.resolution["value"])
        validate_non_negative(self.wavelength["value"])
        validate_non_negative(self.z["value"])
        validate_non_negative(self.w0["value"])
    
    def ras(self):
        log_info("Generating Basic Beam Rasterized Field...")
        temp = GBeam_ras(
            plotrange=self.plotrange["value"],
            resolution=self.resolution["value"],
            wavelength=self.wavelength["value"],
            z=self.z["value"],
            w0=self.w0["value"]
        )
        log_info("Basic Beam Rasterized Field Generated.")
        return temp

class Laguerre_Gaussian_Beam(Gaussian_Beam):

    def __init__(
            self,
            l: int = 1,
            p: int = 0,
            **kwargs
            ):
        super().__init__(**kwargs)
        self.beam_type["value"] = "Laguerre-Gaussian"
        self.l = parameter(
            para="Azimuthal Index",
            value=l,
            unit=None
            )
        self.p = parameter(
            para="Radial Index",
            value=p,
            unit=None
            )
        validate_non_negative(self.plotrange["value"])
        validate_non_negative(self.resolution["value"])
        validate_non_negative(self.wavelength["value"])
        validate_non_negative(self.z["value"])
        validate_non_negative(self.w0["value"])
        validate_non_negative(self.l["value"])
        validate_non_negative(self.p["value"])
    
    def ras(self):
        log_info("Generating Basic Beam Rasterized Field...")
        temp = LGBeam_ras(
            plotrange=self.plotrange["value"],
            resolution=self.resolution["value"],
            wavelength=self.wavelength["value"],
            z=self.z["value"],
            w0=self.w0["value"],
            l=self.l["value"],
            p=self.p["value"]
        )
        log_info("Basic Beam Rasterized Field Generated.")
        return temp
    
