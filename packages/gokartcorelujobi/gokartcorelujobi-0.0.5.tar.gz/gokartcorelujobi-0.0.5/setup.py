from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version(filename):
    import ast

    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


install_requires = [
]

module = 'gokart_core'
package = 'gokartcorelujobi'
src = 'src'

version = get_version(filename=f'{src}/{module}/__init__.py')

setup(
    name=package,
    package_dir={'': src},
    packages=[module],
    version=version,
    author='IDSC Frazzoli',
    author_email='idscgokart@gmail.com',
    url='https://github.com/idsc-frazzoli/gokart-core',
    long_description=long_description,
    zip_safe=False,
    install_requires=install_requires,
)