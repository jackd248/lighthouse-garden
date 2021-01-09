import setuptools
import sys
from lighthouse_garden import info

if sys.version_info < (3, 5):
    sys.exit('lighthouse_garden requires Python 3.5+ to run')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lighthouse_garden-kmi',
    version=info.__version__,
    author='Konrad Michalik',
    author_email='support@konradmichalik.eu',
    description='Monitoring performance data by Google Lighthouse.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=info.__homepage__,
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Intended Audience :: Developers'
    ],
    python_requires='>=3.5',
    install_requires=[
        "future-fstrings>=1.2",
        "Jinja2>=2.11.2",
        "anybadge>=1.7.0"
    ],
    entry_points={
        'console_scripts': [
            'lighthouse_garden = lighthouse_garden.__main__:main'
        ]
    },
)
