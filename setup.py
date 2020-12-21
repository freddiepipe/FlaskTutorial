import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='flaskr-freddiepipe',
    version='0.0.1',
    author='Freddie Pipe',
    author_email='freddiepipe@gmail.com',
    description='Flask official tutorial app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/freddiepipe/FlaskTutorial',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
