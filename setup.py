import setuptools
import gqylpy_cache as g

with open('README.md', encoding='utf8') as f:
    readme: str = f.read()

setuptools.setup(
    name=g.__name__,
    version='.'.join(str(n) for n in g.__version__),
    author=g.__author__.split()[0],
    author_email=g.__author__.split()[1][1:-1],
    license='Apache 2.0',
    url='http://gqylpy.com',
    project_urls={'Source': g.__source__},
    description="如其名，它实现缓存功能，可缓存某个函数或某个类中定义的所有方法的返回值。",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)
