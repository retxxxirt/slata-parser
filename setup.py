from distutils.core import setup

setup(
    name='slata-parser',
    packages=['slata_parser'],
    version='0.2.0',
    license='MIT',
    description='Slata shop parser.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    author='retxxxirt',
    author_email='retxxirt@gmail.com',
    url='https://github.com/retxxxirt/slata-parser',
    keywords=['slata', 'slata parser', 'slata api', 'slata crawler'],
    install_requires=['requests==2.23.0', 'beautifulsoup4==4.8.2']
)
