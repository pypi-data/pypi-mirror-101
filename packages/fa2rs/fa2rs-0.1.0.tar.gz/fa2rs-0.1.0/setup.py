import setuptools
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
	def is_pure(self):
		return False

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="fa2rs",
	version="0.1.0",
	author="Pascal Engélibert",
	author_email="tuxmain@zettascript.org",
	description="Bindings to full Rust ForceAtlas2 implementation",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://framagit.org/ZettaScript/fa2rs-py",
	packages=["fa2rs"],
	package_dir={"": "src"},
	ext_package="fa2rs",
	package_data={"":["*.so"]},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Mathematics"
	],
	keywords="forceatlas2 graph force-directed-graph force-layout",
	python_requires='>=3.6',
	include_package_data=True,
	distclass=BinaryDistribution,
)
