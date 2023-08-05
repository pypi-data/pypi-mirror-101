from setuptools import find_packages, setup
setup(
    name='MailMaker',
    packages=find_packages(include=["MailMaker"], exclude=["tests"]),
    version='0.1.4',
    description='MailMaker used to send mails in different applications',
    author='Niklas Maurer',
    license='MIT',
    keywords = ['mail', 'MailMaker', 'easy mailsending']
)