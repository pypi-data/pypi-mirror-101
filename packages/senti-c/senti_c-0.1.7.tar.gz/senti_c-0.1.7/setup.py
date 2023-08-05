import setuptools

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="senti_c", 
    version="0.1.7",
    keywords='traditional chinese, sentiment analysis, BERT, transformer, transfer learning',
    author="Julie Tu and Hsin-min Lu",
    author_email="luim@ntu.edu.tw",
    description="Traditional Chinese sentiment analysis tool based on BERT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hsinmin/senti_c",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        'Topic :: Software Development :: Build Tools',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[
        'transformers==2.11.0',
        'scipy==1.4.1',
        'pandas',
        'scikit-learn',
        'torch>1.0,<1.9.9',
        'tensorflow==2.2.0',
    ],
)
