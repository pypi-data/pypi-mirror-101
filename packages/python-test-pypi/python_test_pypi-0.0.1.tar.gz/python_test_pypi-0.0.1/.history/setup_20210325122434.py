from setuptools import setup, find_packages

# Set the library's long description to the repo's README.md
with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

requirements = ['requests>=2']

setup(
    name='python_core',
    version='0.0.1',
    author='Benjamin Bouchet',
    author_email='<YOUR_EMAIL>',
    description='http client that abstracts calls to API endpoints \
            and handles all errors by raising comprehensible and descriptive \
            exceptions for both http and API errors.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/randoum/python_core',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        # Classifiers for the package
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)