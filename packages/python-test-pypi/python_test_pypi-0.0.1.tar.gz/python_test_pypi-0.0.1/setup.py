from setuptools import setup, find_packages

# Set the library's long description to the repo's README.md
with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = ['requests>=2']

setup(
    name='python_test_pypi',
    version='0.0.1',
    author='test user',
    author_email='test_user@pptest.com',
    description='http client \
            handles all errors \
            exceptions ',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/N950/test_pypi.git',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        # Classifiers for the package
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)