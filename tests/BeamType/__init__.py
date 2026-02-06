# /beamtype/__init__.py

# 1.批量导入 - 简化导入路径
from .api import Plain_Beam as PBeam
from .api import Gaussian_Beam as GBeam
from .api import Laguerre_Gaussian_Beam as LGBeam

# 2.定义__all__ - 控制导入内容
__all__ = ["PBeam", "GBeam", "LGBeam"]

# 3.共享包级变量、配置、函数

#   包级版本信息
__version__ = "0.1.0"

#   包级配置信息
config = {
    "debug":False,
    "max_resolution":4096
}

#   包级函数
def get_BeamType_varsion():
    return "BeamType v" + __version__