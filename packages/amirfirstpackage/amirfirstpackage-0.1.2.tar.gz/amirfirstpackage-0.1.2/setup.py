from setuptools import setup, find_packages


setup_args = dict(
    name='amirfirstpackage',
    version='0.1.2',
    description='Useful tools to work with Elastic stack in Python',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Amirhossein Yousefi',
    author_email='amir.usefi75@gmail.com',
    keywords=['Elastic', 'ElasticSearch', 'ElasticStack'],
    url='https://github.com/ncthuc/elastictools',
    download_url='https://pypi.org/project/elastictools/'
)

install_requires = [
    'elasticsearch>=6.0.0,<7.0.0',
    'jinja2'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)