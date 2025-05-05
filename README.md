<h1 align="center">objdbg：一款专注于python object的调试器</h1>
<p align="center">
<img src=https://img.shields.io/badge/python-3-blue?style=for-the-badge>
<img src=https://img.shields.io/badge/License-Apache2.0-green?style=for-the-badge>
<img src=https://img.shields.io/badge/State-Developing-red?style=for-the-badge>
<em><h5 align="center"></h5></em>

>objdbg目前尚处于开发阶段。功能尚不完整。

# 简介
## 什么？
objdbg是一款专门用于python object的调试器。它可以使你轻松地在交互式的shell中对一个特定的python object进行静态和动态的分析。
## 等等，什么？？？
假设存在如下object：
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
我们可以使用objdbg对其进行调试，如下：
```python
from objdbg import dbg
dbg(A())
```
就会弹出如下交互式的shell。
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
可以使用objdbg内置的命令对该object进行调试。

# 功能

## 静态

**objprint**：列出object的所有属性&方法，每次调用`dbg()`时会自动调用。  

![1.png](https://img.picui.cn/free/2025/04/30/68121c4b7bcb3.png)

**func**：列出object中内置的所有函数（包括**重写过的**魔术方法）及其参数。  

![2.png](https://img.picui.cn/free/2025/04/30/6812095fef37b.png)

**attr**：列出object中的所有属性。

![1746365505015.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.7snfab9ai0.png)

**pickle**：输出pickle.dumps(obj)并进行base64编码。  

![1746017492227.png](https://img.picui.cn/free/2025/04/30/68121cd74fbec.png)

**obj.{attr}**：打印obj对应的属性

![1746020496532.png](https://img.picui.cn/free/2025/04/30/681228941b2f5.png)

**dir {obj.xxx}**：打印dir(obj.xxx)，假如不传参默认dir(obj)

![1746365084603.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.4ub56t236u.png)

**func {funcname} {arg1} {arg2} ......**：调用object内的函数，输出返回值。  

![1746365587646.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.6iki405lnj.png)

**TODO** **note**：快速列出object中比较值得注意的信息。（eg：被修改的魔术方法）  


......

## 动态

**shell**：切换到python interactive shell。本地命名空间中含有接受调试的object。

![1746017961019.png](https://img.picui.cn/free/2025/04/30/68121eac7305f.png)

**mod_attr {attrname} {new_value}**：修改object内的特定属性。支持元组，列表，字典的各种嵌套。  

![1746017871028.png](https://img.picui.cn/free/2025/04/30/68121e52aa4fd.png)

**reset**：将调试器内的object恢复成一开始传入调试器的object。    

![1746018930045.png](https://img.picui.cn/free/2025/04/30/68122277e5607.png)

**retr**：停止调试，返回调试器内的object。    

**exit&quit**：停止调试，返回None。  

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

**del attr {attrname}**：删除object内的特定属性。  

**del func {funcname}**：屏蔽object内的特定方法。

> note: 由于python中不能直接从实例中删除方法，所以当你尝试del一个方法时，objdbg会将其定义为None，使其成为notcallable。但是，这个属性不会消失。

![1746019837926.png](https://img.picui.cn/free/2025/04/30/68122600730a8.png)

**TODO** **mod_func {funcname} {base64_code}**：修改&新建object的特定方法（将代码base64编码后传入）。  

## 其他

**help**：打印帮助信息

![1746365894752.png](https://github.com/LamentXU123/picx-images-hosting/raw/master/image.6m441pv836.png)

# 安装

```bash
pip install objdbg
```

# 协议

objdbg项目基于Apache Lisence 2.0。

# bug报告&贡献

如果你在使用objdbg时发现了bug，请在issue中告知我，或者联系lamentxu@163.com。谢谢！

如果你对这个项目感兴趣的话，也欢迎在我的邮箱中联系我。objdbg正处于开发的初期阶段，我非常期待得到你的帮助！


