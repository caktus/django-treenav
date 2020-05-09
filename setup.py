from setuptools import setup, find_packages

setup(
    name='django-treenav',
    version=__import__('treenav').__version__,
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    url='https://github.com/caktus/django-treenav',
    license='BSD',
    description='Extensible, hierarchical, and pluggable navigation system '
                'for Django sites',
    zip_safe=False,  # because we're including media that Django needs
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.rst').read(),
    install_requires=[
        "django-mptt>=0.11.0",
    ],
)
