# setup.py
from setuptools import setup, find_packages

setup(
    name="video2slides",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        # 列出你的包依赖项
        "scenedetect",
        "typer",
        "python-pptx",
        "pillow",
    ],
    entry_points={
        'console_scripts': [
            'video2slides=video2slides.main:app',
        ],
    },
)