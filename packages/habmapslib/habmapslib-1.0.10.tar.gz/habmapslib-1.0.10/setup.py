
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="habmapslib",
    include_package_data=True,
    version="1.0.10",
    author="Alpeza",
    author_email="",
    description="Librería para el acceso a habmaps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpeza/habmapsgateway",
    packages=setuptools.find_packages(),
    install_requires=[
        'paho_mqtt>=1.5.1',
        'click>=7.1.2',
        'PyYAML>=3.11'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires='>=3.6, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/alpeza/habmapsgateway/issues',
        'Funding': 'https://github.com/alpeza/habmapsgateway/issues',
        'Say Thanks!': 'https://github.com/alpeza/habmapsgateway/issues',
        'Source': 'https://github.com/alpeza/habmapsgateway',
    },
) 
