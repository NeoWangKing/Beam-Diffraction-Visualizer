# /BeamType/algorithms/__init__.py

# 1.批量导入 - 简化导入路径
from .rasterized import Basic_Beam_rasterized as BBeam_ras
from .rasterized import Gaussian_Beam_rasterized as GBeam_ras
from .rasterized import Laguerre_Gaussian_Beam_rasterized as LGBeam_ras

# 2.定义__all__ - 控制导入内容
__all__ = ["BBeam_ras", "GBeam_ras", "LGBeam_ras"]

# 3.共享包级变量、配置、函数

#   包级版本信息
__version__ = "0.1.0"

#   包级配置信息

#   包级函数
def get_algorithms_version():
    return "Algorithms v" + __version__