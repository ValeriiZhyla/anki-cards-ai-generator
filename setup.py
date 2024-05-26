from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name='anki-cards-ai-generator',
    version='0.1.0',
    install_requires=read_requirements(),
    python_requires='>=3.10',
    url='https://github.com/ValeriiZhyla/anki-cards-ai-generator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
