from setuptools import setup, find_packages

setup(
    name='pywebsdr',
    version='1.0.0',
    description='Python Web SDR',
    long_description='Python Web SDR',
    url='https://github.com/matusnovak/pywebsdr',
    author='Matus Novak',
    author_email='matusnov@gmail.com',
    license='MIT',
    keywords='sdr',
    packages=find_packages(),
    install_requires=['Flask', 'flask_socketio', 'eventlet', 'numpy'],
    entry_points={
        'console_scripts': [
            'pywebsdr=pywebsdr.__init__:main',
        ],
    },
)
