import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="kama-sdk-py",
  version="0.0.002",
  author="Nectar Cloud Software",
  author_email="xavier@codenectar.com",
  description="Kubernetes Application Management API (KAMA) SDK",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/nectar-cs/kama-sdk-py",
  packages=setuptools.find_packages(exclude=[
    "kama_sdk.tests.*",
    "kama_sdk.tests"
  ]),
  package_data={
    'kama_sdk': [
      'assets/*.*'
      'model/**/yamls/*'
    ]
  },
  include_package_data=True,
  install_requires=[
    'flask>=1.1',
    'flask-cors',
    'k8kat>=0.0.228',
    'requests',
    'termcolor>=1.1.0',
    'pymongo',
    'cachetools>=3.1',
    'redis>=3',
    'rq',
    'validators',
    'humanize>=3.2.0',
    'jq>=1.1.2'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.8'
)
