<h1 align="center">objdbg: a debugger focused on python object</h1>
<p align="center">
<img src=https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge>
<img src=https://img.shields.io/badge/License-Apache2.0-green?style=for-the-badge>
<img src=https://img.shields.io/badge/State-Developing-red?style=for-the-badge>
<em><h5 align="center"></h5></em>

# Install

```bash
pip install objdbg
```


# Introduction
## What?
objdbg is a debugger specially used for python object. It allows you to easily perform static and dynamic analysis of a specific python object in an interactive shell.
## Wait, what? ? ?
Assume that there is the following object:
```python
class A():
    def __init__(self):
        self.s = 1
    def __eq__(self):
        return False

    @staticmethod
    def staticadd(b, v):
        return b + v
    @classmethod
    def classadd(self, c, b=1, v=2):
        return b + v + c
    def add(self, a, b, c, *args, **kargs):
        return a + b + c
```
We can debug it using objdbg, as follows:
```python
from objdbg import dbg
dbg(A())
```
The following interactive shell will pop up.
```bash
python OBJect DeBuGger (OBJDBG) v0.1

[*] Details of the object (command "objprint"):

<A 0x29f26895190
  def add(a, b, c, *args, **kargs),
  def classadd(c, b=1, v=2),
  .s = 1,
  .staticadd = <function staticadd>

objdbg>
```
This object can be debugged using objdbg built-in commands.

# Function

## Static

**objprint**: List all properties & methods of object, each call`dbg()`will be called automatically.

![1.png](https://img.picui.cn/free/2025/04/30/68121c4b7bcb3.png)

**func**: Lists all built-in functions (including ** rewrite ** magic methods) and their parameters.

![2.png](https://img.picui.cn/free/2025/04/30/6812095fef37b.png)

**attr**: Lists all attributes in the object.

![1746365505015.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.7snfab9ai0.png)

**pickle**: Output pickle.dumps(obj) and perform base64 encoding.

![1746017492227.png](https://img.picui.cn/free/2025/04/30/68121cd74fbec.png)

**obj.{attr}**: Print the corresponding attributes of obj

![1746020496532.png](https://img.picui.cn/free/2025/04/30/681228941b2f5.png)

**dir {obj.xxx}**: Print dir(obj.xxx), if the parameter is not passed, the default dir(obj)

![1746365084603.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.4ub56t236u.png)

**func {funcname} {arg1} {arg2} ......**: Call the function in object and output the return value.

![1746365587646.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.6iki405lnj.png)

**TODO** **note**: Quickly list more noteworthy information in the object. (eg: modified magic method)


......

## dynamic

**shell**: Switch to python interactive shell. The local namespace contains an object that accepts debugging.

![1746017961019.png](https://img.picui.cn/free/2025/04/30/68121eac7305f.png)

**mod_attr {attrname} {new_value}**: Modify specific attributes within the object. Supports various nesting of tuples, lists, and dictionaries.

![1746017871028.png](https://img.picui.cn/free/2025/04/30/68121e52aa4fd.png)

**reset**: Restore the object in the debugger to the object passed to the debugger at the beginning.

![1746018930045.png](https://img.picui.cn/free/2025/04/30/68122277e5607.png)

**retr**: Stop debugging and return to the object in the debugger.

**exit&quit**: Stop debugging and return None.

```python
from objdbg import dbg
class A():
    def __init__(self):
        self.s = 1
    def __eq__(self):
        return False

    @staticmethod
    def staticadd(b, v):
        return b + v
    @classmethod
    def classadd(self, c, b=1, v=2):
        return b + v + c
    def add(self, a, b, c, *args, **kargs):
        return a + b + c
n = dbg(A)
# if retr: n == A_that_is_modified_in_debugger
# if exit&quit: n == None
```

**del attr {attrname}**: Delete specific attributes in object.

**del func {funcname}**: Block specific methods within an object.

> note: Since methods cannot be deleted directly from instances in python, when you try to del a method, objdbg will define it as None, making it notable. However, this property will not disappear.

![1746019837926.png](https://img.picui.cn/free/2025/04/30/68122600730a8.png)

**TODO** **mod_func {funcname} {base64_code}**: A specific method to modify & create a new object (pass the code base64 after encoding).

## other

**help**: Print help information

![1746365894752.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.6m441pv836.png)

# protocol

The objdbg project is based on Apache Lisence 2.0.

# Bug Reports & Contributions

If you find a bug when using objdbg, please let me know in the issue, or contact lamentxu@163.com. Thanks!

If you are interested in this project, please also contact me in my email. objdbg is in the early stages of development, and I am looking forward to your help!


