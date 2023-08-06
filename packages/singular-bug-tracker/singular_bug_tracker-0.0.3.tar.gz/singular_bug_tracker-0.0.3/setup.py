import setuptools

setuptools.setup(
    name='singular_bug_tracker',
    version='0.0.3',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Bug tracker',
    long_description='Bug tracker',
    url='https://lucas@bitbucket.org/singular-dev/bug_tracker.git',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'django',
    ]
)
