from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='processdat',
	version='0.0.1',
	description='Data preprocessing for ML, returns X_train, X_test, y_train, y_test',
	py_modules=["processdat"],
	package_dir={'': 'src'},

	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],

	long_description=long_description,
	long_description_content_type="text/markdown",

	install_requires=[
		"numpy>=1.19.2",
		"pandas>=1.1.3",
		"scikit-learn>=0.22.0",	
	],

	extra_require = {
		"dev": [
			"pytest>=3.7",
		],
	},

	url="https://github.com/ShayanBanerjee/processdat.git",
	author="Shayan Banerjee",
	author_email="shayanbanerjee96@gmail.com",
)