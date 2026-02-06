# /BeamType/algorithms/__init__.py

# 1.批量导入 - 简化导入路径
from .core import gender_intensity as gen_i
from .core import gender_phase as gen_p

# 2.定义__all__ - 控制导入内容
__all__ = ["gen_i", "gen_p"]

# 3.共享包级变量、配置、函数

#   包级版本信息
__version__ = "0.1.0"

#   包级配置信息

#   包级函数
def get_gender_version():
    return "Gander v" + __version__