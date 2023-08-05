from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ML-DL-implementation',
    packages=['MLlib'],
    version='1.0.1',
    license='BSD-3',
    author="Robotics Society IITJ",
    author_email="singh.77@iitj.ac.in",
    description="Package for ML and DL algorithms using nothing but numpy and matplotlib.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/RoboticsClubIITJ/ML-DL-implementation",
    download_url='https://github.com/RoboticsClubIITJ/ML-DL-implementation/archive/refs/tags/1.0.1.tar.gz',
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.0',
        'matplotlib>=3.0.0',
        'scipy'
        'pandas'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
