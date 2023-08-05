import setuptools

f = open("readme.md")
descriptionlol = f.read()

setuptools.setup(
name="hentaihavenpy",
version="0.2",
author="hentaihaven.edu",
description="haha hentai api go brrrrrrrrr cumshot in my ass",
long_description=descriptionlol,
long_description_content_type="text/markdown",
url="https://hentaihaven.dev",
package_dir={"": "hentaihavenpy"},
packages=setuptools.find_packages(where="hentaihavenpy"),
install_requires=["requests"]
)