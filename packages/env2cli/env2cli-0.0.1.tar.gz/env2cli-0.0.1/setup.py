import setuptools

setuptools.setup(
    name='env2cli',
    version="0.0.1",
    author="Aviv Abramovich",
    author_email="AvivAbramovich@gmail.com",
    description="Converts environment variables into cli arguments for easy maintainable docker entry point",
    url="https://github.com/AvivAbramovich/Env2Cli",
    project_urls={
        "Bug Tracker": "https://github.com/AvivAbramovich/Env2Cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)