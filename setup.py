from setuptools import setup, find_packages
setup(name='jackcast',
      version='0.0.1',
      description='',
      author='William Koch',
      author_email='wfkoch [at] gmail [dot] com',
      url='https://github.com/wil3/jackcast',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['wheel', 'soco', 'Flask', 'gunicorn', 'greenlet', 'gevent']
)
