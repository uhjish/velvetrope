from setuptools import setup, find_packages
setup(
    name = "VelvetRope",
    version = "0.1",
    packages = find_packages(),
    scripts = ['velvetrope.py'],

    install_requires = ['argparse','psutil'],

    package_data = {
    },

    # metadata for upload to PyPI
    author = "Ajish George",
    author_email = "ajish@rootedinsights.com",
    description = "Allows for opportunistic memory-limited running of tasks in parallel.",
    license = "WTFPL"

    # could also include long_description, download_url, classifiers, etc.
)
