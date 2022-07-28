[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Version](https://img.shields.io/pypi/v/gqylpy_cache)](https://pypi.org/project/gqylpy_cache/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_cache)](https://pypi.org/project/gqylpy_cache)
[![License](https://img.shields.io/pypi/l/gqylpy_cache)](https://github.com/gqylpy/gqylpy-cache/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_cache/month)](https://pepy.tech/project/gqylpy_cache)

# gqylpy-cache

> 如其名，`gqylpy_cache` 实现缓存功能，由 GQYLPY 团队研发的一个框架，可缓存某个函数或某个类中定义的所有方法的返回值。
> 
> > 你一定遇到过这样的情况：你的程序中有一个函数会被多次调用，并且返回值不变。你会怎么做？为提高代码效率，你会先调用一次该函数并把返回值存到一个变量，之后就使用这个变量，而不是重复调用函数。是这样吗？那太Low了。现在，我们传授你一种更高明的方案。使用 `gqylpy_cache` 模块，直接缓存函数返回值。
> 
> `gqylpy_cache` 有两种使用方式：当做元类使用，将缓存其元类实例中定义的所有方法的返回值；当做装饰器使用，将缓存被装饰函数的返回值。

<kbd>pip3 install gqylpy_cache</kbd>

###### 缓存类中方法的返回值

```python
import gqylpy_cache

class Alpha(metaclass=gqylpy_cache):
    ...
```
此时，类 `Alpha` 中定义的所有方法以及`property`属性，在被其实例调用一次后，其返回值都将被缓存，缓存在 `__cache_pool__` 属性中。此后的每次调用，只要参数不变，都是直接从 `__cache_pool__` 中取值，不会重复执行相关代码，大幅减少程序功耗并提高代码可读性。

上述缓存功能默认只作用于单个实例，每个实例都有自己的 `__cache_pool__` 属性，若希望 `Alpha` 的所有实例共享同一份缓存，可启用 `__shared_instance_cache__` 属性：
```python
class Alpha(metaclass=gqylpy_cache):
    __shared_instance_cache__ = True
```
设置类属性 `__shared_instance_cache__ = True` 后，属性 `__cache_pool__` 将被创建在 `Alpha` 类中，而不是 `Alpha` 的每个实例中。

若希望某个方法或`property`不被缓存，可将其加入到 `__not_cache__` 列表中：

```python
class Alpha(metaclass=gqylpy_cache):
    __not_cache__ = [method_obj_or_method_name, ...]
```
另外，`Alpha` 的子类也拥有上述缓存功能。

###### 缓存函数返回值

```python
import gqylpy_cache

@gqylpy_cache
def alpha():
    ...
```
此时，函数 `alpha` 在被调用一次后，其返回值将被缓存。此后的每次调用，只要参数不变，都是直接从缓存中取值，而不会重复执行 `alpha` 函数。

另外一种兼容编辑器语法提示的用法：
```python
from gqylpy_cache import cache

@cache
def alpha():
    ...
```
