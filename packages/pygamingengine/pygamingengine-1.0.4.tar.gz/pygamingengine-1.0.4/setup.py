from setuptools import setup

VERSION = '1.0.4'
DESCRIPTION = 'A game engine'

requires = open('requirements.txt', 'r').read().splitlines()

# Setting up
setup(
    name="pygamingengine",
    version=VERSION,
    author="abhra2020smart (Abhradeep De)",
    author_email="deabhradeep@gmail.com",
    description=DESCRIPTION,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
