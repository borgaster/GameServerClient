from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='GameServerClient',
    version='0.1',
    description='Server/Client platform for games',
    url='https://github.com/borgaster/GameServerClient.git',
    author='Andre Bastos',
    author_email='bastos.33296@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Network',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.7',

    ],
    keywords='podsixnet Network Game',
    packages=find_packages(),
    install_requires=["podsixnet"],

)