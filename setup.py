"""TODO: Long description
"""

from setuptools import setup


setup(
    name='yield-for-cache',
    version='0.0.1',
    description='TODO',
    long_description=__doc__,
    url='https://github.com/youtux/yield-for-cache',
    author='Alessio Bogon',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Web Environment',

        'Intended Audience :: Developers',

        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=['yield_for_cache'],
    install_requires=[
        'Flask',
    ],
    extras_require={
        'test': [
            'mock',
            'coverage',
            'pytest',
            'pytest-cov',
            'pytest-pep8',
        ],
    },
)