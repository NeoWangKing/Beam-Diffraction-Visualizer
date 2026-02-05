# BeamType/__init__.py

# 1.批量导入 - 简化导入路径
from .api import *

# 2.定义__all__ - 控制导入内容
__all__ = []

# 3.共享包级变量、配置、函数

# 包级配置信息
__version__ = "0.1.0"

config = {
    "debug":False
}