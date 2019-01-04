from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='STALKER',
    version='0.0.1',
    description='Slackbot for following users on social platforms',
    long_description=readme,
    author='Michael Dunn',
    author_email='mikey.dunn@yahoo.com',
    url='https://github.com/MikeyDunn/S.T.A.L.K.E.R.',
    license=license,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stalker=src.main:main',
        ]
    }
)
