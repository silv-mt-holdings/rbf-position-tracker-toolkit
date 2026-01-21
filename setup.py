from setuptools import setup, find_packages

setup(
    name="rbf-position-tracker-toolkit",
    version="1.0.0",
    author="Silv MT Holdings",
    description="RBF position tracking toolkit - Detects existing RBF payments, calculates stacking risk, and payment patterns",
    url="https://github.com/silv-mt-holdings/rbf-position-tracker-toolkit",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=[
        "transaction-classifier-toolkit",
    ],
    extras_require={"dev": ["pytest>=7.0.0"]},
)
