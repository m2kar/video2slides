# Copyright (c) 2024 m2kar
# Created: 2024/12/01
# Author: m2kar <m2kar.cn#gmail.com>
# License: MIT
# File: setup.py
# Description: setup.py for video2slides

# setup.py
from setuptools import setup, find_packages

setup(
    name="video2slides",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        # 列出你的包依赖项
        "scenedetect",
        "typer",
        "python-pptx",
        "pillow",
        "openai-whisper"
    ],
    entry_points={
        'console_scripts': [
            'video2slides=video2slides.main:app',
        ],
    },
)