from setuptools import setup

VERSION = '1.0.6'
DESCRIPTION = 'A (simple) game engine'

requires = open('requirements.txt', 'r').read().splitlines()

# Setting up
setup(
    name="pygamingengine",
    version=VERSION,
    author="abhra2020smart (Abhradeep De)",
    author_email="deabhradeep@gmail.com",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
