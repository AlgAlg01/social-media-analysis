from setuptools import setup, find_packages

setup(
    name="social-media-analysis",
    version="0.1.0",
    author="G/Ker(f)≅Im(f)",
    description="A tool for analyzing social media trends and content performance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlgAlg01/social-media-analysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "praw>=7.4.0",
        "tweepy>=4.0.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "social-analysis=src.main:main",
        ],
    },
)