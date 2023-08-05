import setuptools

setuptools.setup(
    name='singular_server_updater',
    version='0.0.1',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Server updater',
    long_description='Server updater',
    url='https://lucas@bitbucket.org/singular-dev/server_updater.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'django',
        'fabric',
        'invoke',
    ]
)
