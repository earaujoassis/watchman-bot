import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="watchman-bot",
    version="0.2.4",
    license="MIT",
    author="Ewerton Carlos Assis",
    author_email="earaujoassis@gmail.com",
    description="Watchman helps to keep track of automating services; a tiny bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/earaujoassis/watchman-bot",
    packages=setuptools.find_packages(exclude=[
        'internal',
        '.editorconfig',
        '.gitignore',
        '.tool-versions',
        '.travis.yml',
        'go.mod',
        'go.sum',
        'main.go',
    ]),
    install_requires=[
        'Mako',
        'argparse',
        'requests',
    ],
    python_requires='>=2.7, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        'agents': ['templates/*'],
    },
    entry_points={
        'console_scripts': [
            'agent=agents:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/earaujoassis/watchman-bot',
        'Tracker': 'https://github.com/earaujoassis/watchman-bot/issues',
    },
)
