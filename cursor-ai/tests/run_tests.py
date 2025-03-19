import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所有测试
from test_solvers import TestSolvers

if __name__ == '__main__':
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSolvers)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite) 