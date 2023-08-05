import setuptools
with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "Swifter in NLP Fake News Identification",
	version = "0.0.1",
	author = "Sagnik Sarkar",
	email = "sagniksarkar.agt@gmail.com",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=['GoogleNews', 'newspaper3k', 'pandas','nltk'],
    keywords=['python', 'NLP', 'News Paper', 'Fake News', 'NLP News'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
	)