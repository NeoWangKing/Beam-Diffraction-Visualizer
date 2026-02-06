# /BeamType/api.py

#导入内部工具模块
from .utils import log_info, log_warning, log_error, validate_2_num, validate_2_int, validate_2_float, validate_input, validate_non_negative
#导入算法模块
from .algorithms import PBeam_ras, GBeam_ras, LGBeam_ras
from .gender import gen_i, gen_p

class Beam():

    def __init__(
            self,
            plotrange: str = "1e-2",
            resolution: str = "1024",
        ):
        '''Handle Variables'''
        self.beam_type = {
            "para": "Beam Type",
            "value": "Basic",
            "unit": None
            }
        
        log_info("Validating data: plotrange")
        validate_input(plotrange)
        validate_2_float(plotrange)
        validate_non_negative(float(plotrange))
        self.plotrange = {
            "para": "Plot Range",
            "value": float(plotrange),
            "unit": "m"
            }
        
        log_info("Validating data: resolution")
        validate_input(resolution)
        validate_2_int(resolution)
        validate_non_negative(int(resolution))
        self.resolution = {
            "para": "Resolution",
            "value": int(resolution),
            "unit": "px"
            }

    def ras(self):
        log_info("This is the beam-rasterize template")
        return None
    
    def plot_intensity(self, disp: bool = False, deta: bool = False):
        gen_i(self.ras(), disp=disp, deta=deta)

    def plot_phase(self, disp: bool = False, deta: bool = False):
        gen_p(self.ras(), disp=disp, deta=deta)

    
    def get_paras(self) -> dict:
        log_info("Getting parameters of Beam")
        return self.__dict__


class Plain_Beam(Beam):

    def __init__(
            self,
            wavelength: str = "632.8e-9",
            z: str = "1.0",
            **kwargs
        ):
        '''Handle Variables'''
        super().__init__(**kwargs)
        self.beam_type = {
            "para": "Beam Type",
            "value": "Plain",
            "unit": None
            }
        
        log_info("Validating data: wavelength")
        validate_input(wavelength)
        validate_2_float(wavelength)
        validate_non_negative(float(wavelength))
        self.wavelength = {
            "para": "Wavelength",
            "value": float(wavelength),
            "unit": "m"
            }
        
        log_info("Validating data: z")
        validate_input(z)
        validate_2_float(z)
        validate_non_negative(float(z))
        self.z = {
            "para": "Propagation Distance",
            "value": float(z),
            "unit": "m"
            }

    def ras(self):
        log_info("Generating Plain Beam Rasterized Field...")
        temp = PBeam_ras(
            plotrange = self.plotrange["value"],
            resolution = self.resolution["value"],
            wavelength = self.wavelength["value"],
            z = self.z["value"]
        )
        log_info("Plain Beam Rasterized Field Generated.")
        return temp

class Gaussian_Beam(Plain_Beam):

    def __init__(
            self,
            w0: str = "1e-3",
            **kwargs
        ):
        '''Handle Variables'''
        super().__init__(**kwargs)
        self.beam_type["value"] = "Gaussian"

        log_info("Validating data: w0")
        validate_input(w0)
        validate_2_float(w0)
        validate_non_negative(float(w0))
        self.w0 = {
            "para": "Beam Waist",
            "value": float(w0),
            "unit": "m",
            }
    
    def ras(self):
        log_info("Generating Basic Beam Rasterized Field...")
        temp = GBeam_ras(
            plotrange = self.plotrange["value"],
            resolution = self.resolution["value"],
            wavelength = self.wavelength["value"],
            z = self.z["value"],
            w0 = self.w0["value"]
        )
        log_info("Basic Beam Rasterized Field Generated.")
        return temp

class Laguerre_Gaussian_Beam(Gaussian_Beam):

    def __init__(
            self,
            l: str = "1",
            p: str = "0",
            **kwargs
        ):
        '''Handle Variables'''
        super().__init__(**kwargs)
        self.beam_type["value"] = "Laguerre-Gaussian"

        log_info("Validating data: l")
        validate_input(l)
        validate_2_int(l)
        validate_non_negative(int(l))
        self.l = {
            "para": "Azimuthal Index",
            "value": int(l),
            "unit": None
            }
        
        log_info("Validating data: p")
        validate_input(p)
        validate_2_int(p)
        validate_non_negative(int(p))
        self.p = {
            "para": "Radial Index",
            "value": int(p),
            "unit": None
            }
    
    def ras(self):
        log_info("Generating Basic Beam Rasterized Field...")
        temp = LGBeam_ras(
            plotrange = self.plotrange["value"],
            resolution = self.resolution["value"],
            wavelength = self.wavelength["value"],
            z = self.z["value"],
            w0 = self.w0["value"],
            l = self.l["value"],
            p = self.p["value"]
        )
        log_info("Basic Beam Rasterized Field Generated.")
        return temp
    
