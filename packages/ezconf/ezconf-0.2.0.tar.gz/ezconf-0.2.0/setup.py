from distutils.core import setup

setup(
    name="ezconf",
    packages=["ezconf"],
    version="0.2.0",
    license="MIT",
    description="An easy-to-use configuration package using YAML",
    author="Lars Eppinger",
    author_email="pypi@eppinger.dev",
    url="https://github.com/lars250698/easyconfig",
    download_url="https://github.com/lars250698/ezconf/archive/v_0_2_0.tar.gz",
    keywords=["config", "configuration", "yaml", "easyconfig", "easyconf", "ezconfig", "ezconf"],
    requires=["pyyaml"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)