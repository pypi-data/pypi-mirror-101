from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name='LastDB',
    version='0.1.2',
    author='MikaelStave',
    author_email='mikael.stave@gmail.com',
    description="Database using json",
    long_description=readme(),
    packages=["LastDB"],
    license="MIT",
    url=""
)
