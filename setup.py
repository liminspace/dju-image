import os
from distutils.core import setup
from setuptools import find_packages
import dju_image


setup(
    name='dju-image',
    version=dju_image.__version__,
    description='Django Utils: Image Library',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='MIT',
    author='Igor Melnyk',
    author_email='liminspace@gmail.com',
    url='https://github.com/liminspace/dju-image',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,  # because include static
    install_requires=[
        'dju-common',
        'django>=1.8.<1.11',
        'Pillow',
    ],
)
