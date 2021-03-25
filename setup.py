from setuptools import setup, find_packages


__version__ = '1.0.1'

setup(name='vk_maria',
      version=__version__,
      description='vk bot api wrapper',
      long_description=open('README.md', encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/lxstvayne/vk_maria',
      keywords='vk bot tools',
      packages=find_packages(),
      install_requires=[
            'requests>=2.20.1',
            'loguru>=0.5.3',
            'pydotdict>=3.3.11'
      ],
      author='lxstvayne',
      author_email='lxstv4yne@gmail.com',
      zip_safe=False)