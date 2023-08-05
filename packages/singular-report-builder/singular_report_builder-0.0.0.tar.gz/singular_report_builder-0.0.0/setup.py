import setuptools

setuptools.setup(
    name='singular_report_builder',
    # version='0.0.12',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Report builder',
    long_description='Report builder',
    url='https://lucas@bitbucket.org/singular-dev/server_updater.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'django',
        'fabric',
        'invoke',
    ]
)
