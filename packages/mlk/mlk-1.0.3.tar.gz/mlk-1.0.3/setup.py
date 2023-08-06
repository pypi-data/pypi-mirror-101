import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlk",
    version="1.0.3",
    author="Will Nguyen",
    author_email="will.ng.nguyen@gmail.com",
    description="ML Kit",
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
        'redis',
        'requests',
        'openpyxl',

        'brotli',
        'Faker',

        'keras',
        'seaborn',
        'scikit-learn',
        'scikit-image',
        'pandas',
        'matplotlib',
        'opencv-python',
        'tabulate',

        'Pillow',
        'scikit-image',
        'texttable',
        'wordcloud',
        'nltk',

        'imutils',

        'tensorflow==2.3.2', #  cudart64_101.dll
        'numpy==1.18.5',
        'decorator',
    ]
)
