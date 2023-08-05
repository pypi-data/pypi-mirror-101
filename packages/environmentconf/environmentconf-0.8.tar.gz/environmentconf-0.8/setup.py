from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='environmentconf',
    version='0.8',
    description = 'Environment configurator for the distributed systems',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author = 'Maulik Patel',
    author_email = 'maulik.info.tech@gmail.com',
    url = 'https://github.com/maulik887/environmentconf',
    download_url = 'https://github.com/maulik887/environmentconf/archive/refs/tags/0.8.zip',
    keywords = ['Environment', 'Configuration', 'Docker', 'EC2', 'Server'],
    include_package_data=True,
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6'
  ]
)

install_requires = [
    'jsonschema>=3.2.0',
    'pyyaml>=5.4.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)