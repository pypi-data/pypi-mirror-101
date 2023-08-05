from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hydradb',
    version='3.0.0',
    packages=['hydra'],
    url='https://github.com/rhmtazad/hydraDB',
    license='MIT License',
    classifiers=classifiers,
    author='Rahmat Azad',
    author_email='rhmtazad@gmail.com',
    description='An API for faster and easier SQLite/Python operations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['']
)
