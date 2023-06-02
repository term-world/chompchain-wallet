import setuptools

setuptools.setup(
    name="chompchain-wallet",
    version="0.1",
    packages=['chompchainwallet'],
    include_package_data=True,
    description='Wallet for chompchain.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
