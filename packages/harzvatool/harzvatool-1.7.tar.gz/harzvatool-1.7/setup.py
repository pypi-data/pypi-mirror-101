from os.path import dirname, join
# from pip.req import parse_requirements
from setuptools import (
    find_packages,
    setup,
)
def parse_requirements(fname='requirements.txt', with_version=True):
    """Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if True include version specs

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
    """
    import sys
    from os.path import exists
    import re
    require_fpath = fname

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='harzvatool',  # 模块名称
    version=version,
    description="harzva's package",  # 描述
    packages=find_packages(exclude=('configs', 'tools', 'demo')),
    author='harzva',
    author_email='626609967@qq.com',
    license='Apache License v1',
    package_data={'': ['*.*']},
    # include_package_data = True,
    url='http://github.com/tongling/clinicaltrial',
    install_requires=parse_requirements("requirements.txt"),  # 所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)


# 任何包如果包含 *.txt or *.rst 文件都加进去，可以处理多层package目录结构
        # '': ['*.txt', '*.rst'],
# 如果hello包下面有*.msg文件也加进去