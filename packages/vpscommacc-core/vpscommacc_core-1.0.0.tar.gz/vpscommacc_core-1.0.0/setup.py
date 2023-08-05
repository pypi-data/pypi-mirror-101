import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpscommacc_core",
    version="1.0.0",
    author="vpscommacc",
    author_email="vps.commacc@yandex.ru",
    description="Набор полезных функций для повседневной работы и уменьшения размера кода",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vpscommacc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Natural Language :: Russian",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Topic :: Utilities",
    ],
    python_requires='>=3.8',
)
