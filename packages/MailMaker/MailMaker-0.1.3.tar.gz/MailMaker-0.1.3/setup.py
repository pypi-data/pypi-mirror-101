from setuptools import find_packages, setup
setup(
    name='MailMaker',
    packages=find_packages(include=["MailMaker"]),
    version='0.1.3',
    description='MailMaker used to send mails in different applications',
    author='Niklas Maurer',
    license='MIT',
    keywords = ['mail', 'MailMaker', 'easy mailsending']
)