from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='Flask-Hashids',
    version='1.0.1',
    url='https://github.com/Pevtrick/Flask-Hashids',
    author='Patrick Jentsch',
    author_email='patrickjentsch@gmx.net',
    description='Hashids integration for Flask applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['flask_hashids'],
    install_requires=['Flask', 'Hashids >= 1.0.2'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
