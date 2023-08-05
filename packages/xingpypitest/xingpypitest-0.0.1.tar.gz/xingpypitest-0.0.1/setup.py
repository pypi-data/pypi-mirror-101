import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

print(setuptools.find_packages())


setuptools.setup(
    name='xingpypitest',
    version='0.0.1',
    author='XING-ZIWEN',
    author_email='Rick.Xing@Nachmath.com',
    description='The Short Description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://www.baidu.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',

    # package_dir={'': 'xingpypitest'},
    packages=setuptools.find_packages(),

)
