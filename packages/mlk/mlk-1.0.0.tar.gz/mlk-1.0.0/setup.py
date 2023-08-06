import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlk",
    version="1.0.0",
    author="Will Nguyen",
    author_email="will.ng.nguyen@gmail.com",
    description="Machine Learning Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/mlk",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # 'tika',
        'aiohttp',
        'slack_sdk',
        'fake_useragent',

        'beautifulsoup4',
        'mongoengine',
        'redis',
        'peewee',
        'requests',
        'openpyxl',

        'validate_email',
        'validators', # email, url
        'PyExecJS',

        'Pillow',
        'pandas',
        'scikit-image',
        'texttable',
        'wordcloud',
        'nltk',

        'usaddress',
        'us',
        'pyap', # parse addr
        'brotli',
        'cfscrape',
        'Faker',

        'google-auth-oauthlib',
        'google-auth',


        'keras',
        'tensorflow',
        'seaborn',
        'scikit-learn',
        'scikit-image',
        'pandas',
        'matplotlib',
        'opencv-python',
        'tabulate',

        # 'jupyter',
        # 'yapf',  # code prettify
        # 'itkwidgets',
        # 'ipywidgets',
        # 'qgrid',
        # 'jupyterthemes',
        # 'jupyter_nbextensions_configurator',
        # 'jupyter_contrib_nbextensions',

        'favicon',
        'imutils',
        'Pillow',
        'Faker',
        'numpy~=1.19.2',
        'decorator<5',
    ]
)
