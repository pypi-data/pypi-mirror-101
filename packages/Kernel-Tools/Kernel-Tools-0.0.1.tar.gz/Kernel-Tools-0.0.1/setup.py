from setuptools import setup, find_packages

setup (
    name='Kernel-Tools',
    version='0.0.1',
    author="TC Jowers",
    author_email="tyler@earthcomputing.io",

    packages=find_packages(),

    install_requires=[
        'requests',
        'importlib'
    ],

    entry_points={
        "console_scripts": [
            "k=k.__main__:main"
        ]
    }
)