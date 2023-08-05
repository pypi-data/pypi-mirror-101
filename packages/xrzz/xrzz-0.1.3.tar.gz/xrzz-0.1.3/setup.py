from setuptools import setup

with open("README.md", "r") as md:
    desc = md.read()

setup(
    name="xrzz",
    version="0.1.3",
    author="dedshit",
    author_email="crapholy040@gmail.com",
    url="https://www.youtube.com/c/FunnyBunny-YT",
    description="Fast GET/POST HTTP Request",
    py_modules=["xrzz", "sock_HTTP_adapter"],
    package_dir={'': 'src'},
    long_description=desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
