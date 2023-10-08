"""aiookru setup."""
from setuptools import find_packages, setup  # noqa

setup(
    name='aiookru',
    version='1.0.0rc1',
    author='Konstantin Togoi',
    author_email='konstantin.togoi@gmail.com',
    url='https://github.com/konstantintogoi/aiookru',
    project_urls={'Documentation': 'https://konstantintogoi.github.io/aiookru'},
    download_url='https://pypi.org/project/aiookru/',
    description='Python ok.ru API wrapper',
    long_description=open('README.rst').read(),
    license='BSD',
    packages=find_packages(),
    platforms=['Any'],
    python_requires='>=3.7',
    install_requires=['httpx'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest-asyncio', 'pytest-localserver'],
    keywords=['ok.ru rest api asyncio'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)