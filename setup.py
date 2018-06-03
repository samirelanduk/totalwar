from setuptools import setup

setup(
 name="totalwar",
 version="0.1.0",
 description="A TW file parser.",
 url="https://totalwar.samireland.com",
 author="Sam Ireland",
 author_email="mail@samireland.com",
 license="MIT",
 classifiers=[
  "Development Status :: 4 - Beta",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.5",
  "Programming Language :: Python :: 3.6",
 ],
 keywords="chemistry bioinformatics proteins biochemistry molecules PDB XYZ",
 packages=["atomium", "atomium.files", "atomium.structures"],
 install_requires=["numpy", "requests", "rmsd"]
)
