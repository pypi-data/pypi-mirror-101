from setuptools import setup, find_packages

setup(
    name='luktianutl',
    version='0.0.4',
    description=(
        'Utilities For Myself'
    ),
    # long_description=open('README.rst').read(),
    author='luktian',
    author_email='luktian@shu.edu.cn',
    maintainer='luktian',
    maintainer_email='luktian@shu.edu.cn',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    # url='<项目的网址，我一般都是github的url>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'sklearn',
        'numpy',
        'pandas',
        'scipy'
    ]
)