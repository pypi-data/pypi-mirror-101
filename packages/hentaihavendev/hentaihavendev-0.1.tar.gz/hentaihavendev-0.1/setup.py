import setuptools as ok


with open('README.md') as f:
    urmom = f.read()

ok.setup(
    author="https://hentaihaven.dev/",
    author_email="info@hentaihaven.dev",
    name='hentaihavendev',
    license="MIT",
    description='an api wrapper for https://api.hentaihaven.dev/',
    version='v0.1',
    long_description=urmom,
    url='https://github.com/unsecuring/hentaihavendev',
    packages=ok.find_packages(where="hentaihavendev"),
    install_requires=['requests'],
    package_dir={"": "hentaihavendev"},

)