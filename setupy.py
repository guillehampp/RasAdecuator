from setuptools import setup, find_packages

setup(
    name='RasAdecuator',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True, 
    description='Adecua la descarga de la adquisicion para que funciones con el docker de L1SPC',
    long_description=open('README.md').read(),
    author='Guillermo Hampp',
    author_email='ghampp@veng.com.ar',
    url='https://github.com/guillehampp/RasAdecuator',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)