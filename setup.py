import setuptools
import funccache as i

idoc: list = i.__doc__.split('\n')

for index, line in enumerate(idoc):
    if line.startswith('@version: ', 4):
        version = line.split()[-1]
        break
_, author, email = idoc[index + 1].split()
source = idoc[index + 2].split()[-1]

setuptools.setup(
    name=i.__name__,
    version=version,
    author=author,
    author_email=email,
    license='Apache 2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='''
        True to its name, `funccache` implements the cache function. Cache the
        return value of a callable object or all methods defined in a class.
    '''.strip().replace('\n       ', ''),
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[i.__name__],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Artistic Software',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ]
)
