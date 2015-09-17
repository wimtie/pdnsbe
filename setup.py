from setuptools import setup


CUR_VERSION = "0.6.1"

setup(
    name="pdnsbe",
    packages=["pdnsbe"],
    version=CUR_VERSION,
    description="""Library to easily implement and run a python PowerDNS socket
                   backend.""",
    author="Tim Lamballais Tessensohn",
    author_email="peterldowns@gmail.com",
    url="https://github.com/wimtie/pdnsbe",
    download_url="https://github.com/wimtie/pdnsbe/tarball/%s" % CUR_VERSION,
    keywords=["PowerDNS", "backend", "python", "generic", "pluggable"],
    classifiers=[],
)
