import setuptools

with open('requirements.txt', 'r') as fh :
    requirements = fh.read()

with open("README.md", "r") as fh :
    long_description = fh.read()

setuptools.setup(
    name='ds-example-plugin',
    version='1',
    author='Kevin Kramer',
    author_email='kevin.kramer@uzh.ch',
    description='Example plugin for data_slicer`s PIT.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kuadrat/ds_example_plugin.git',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
