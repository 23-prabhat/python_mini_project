from setuptools import setup, find_packages

setup(
    name="git-conflict-resolver",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main", "parser", "resolver", "ai_helper", "utils"],
    entry_points={
        "console_scripts": [
            "gcr=main:main",
        ],
    },
    install_requires=["rich", "colorama", "groq"],
    python_requires=">=3.8",
)
