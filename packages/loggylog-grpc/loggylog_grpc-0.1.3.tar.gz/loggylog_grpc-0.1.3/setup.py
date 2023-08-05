import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("python_reqs.txt", "r", encoding="utf-8") as reqs_file:
    install_requires = list(map(lambda r: r.strip(), reqs_file.readlines()))

setuptools.setup(
    name="loggylog_grpc",
    version="0.1.3",
    author="Vagif Mammadaliyev",
    description="Generated code for loggylog related python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
)
