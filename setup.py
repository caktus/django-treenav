from setuptools import find_packages, setup

setup(
    name="django-treenav",
    version=__import__("treenav").__version__,
    author="Caktus Consulting Group",
    author_email="solutions@caktusgroup.com",
    packages=find_packages(exclude=["example"]),
    include_package_data=True,
    url="https://github.com/caktus/django-treenav",
    license="BSD",
    description="Extensible, hierarchical, and pluggable navigation system "
    "for Django sites",
    zip_safe=False,  # because we're including media that Django needs
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=open("README.rst").read(),
    install_requires=[
        "django-mptt>=0.11.0,<1.0",
    ],
)
