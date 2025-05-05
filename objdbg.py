# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2025/04/30 12:45:40
@Author  :   LamentXU 
'''
import inspect

from objprint import op
from rich.console import Console 
from rich.table import Table
from code import interact
from types import FunctionType
from pickle import dumps
from rich.markdown import Markdown
from copy import deepcopy
from base64 import b64encode
from functools import partial
from typing import Any, Dict
VERSION = '0.1.2.1'
banner = '''
[bold]python [red]OBJ[/red]ect [red]D[/red]e[red]B[/red]u[red]G[/red]ger ([strong][red]OBJDBG[/strong][/red]) v''' + VERSION + '[/bold]\n'
csle = Console()
def is_builtin(obj: Any) -> object:
    """
    检查输入是否为builtins中的内容
    
    参数:
        object obj: 要检查的Python对象
        
    返回:
        bool False: 该对象不为builtins的内容
        object obj: 该对象为builtins的内容
    """
    if isinstance(obj, bool):
        csle.print('[*] Current object is a [strong]bool[/strong] (builtin). Returning it directly.', highlight=False)
        return obj
    elif obj is None:
        csle.print('[*] Current object is [strong]None[/strong] (builtin). Returning it directly.', highlight=False)
        return obj
    elif isinstance(obj, (int, float, str, list, tuple, dict, set)):
        csle.print('[*] Current object is a [strong]'+str(type(obj)).split("'")[1]+'[/strong] (builtin). Returning it directly.', highlight=False)
        return obj
    elif isinstance(obj, FunctionType):
        csle.print('[*] Current object is a [strong]function (<function '+obj.__name__+'>)[/strong]. Returning it directly.', highlight=False)
        return obj
    else:
        return False
def get_methods_with_signatures(obj) -> Dict[str, inspect.Signature]:
    """
    获取对象的所有可调用方法及其签名
    
    参数:
        object obj: 要检查的Python对象
        
    返回:
        dict methods_with_signatures: {方法名，方法的签名对象}
    """
    methods_with_signatures = {}
    
    for name, member in inspect.getmembers(obj):
        if inspect.ismethod(member) or inspect.isfunction(member):
            try:
                sig = inspect.signature(member)
                methods_with_signatures[name] = sig.parameters
            except ValueError or TypeError:
                # 有些内置方法可能无法获取签名
                methods_with_signatures[name] = 'None'

                
    return methods_with_signatures
def get_object_attributes(obj):
    """
    获取对象的所有实例属性（不包括方法）
    
    参数：
        object obj: 要检查的Python对象

    返回:
        字典，键为属性名，值为属性内容
        False, 如果Object不含有__dict__
    
    """
    try:
        return {
            key: value 
            for key, value in vars(obj).items()
            if not callable(value) and not key.startswith('__')
        }
    except TypeError:
        csle.print('Object does not have __dict__ attribute.')
        return False

def get_methods_info(obj: Any) -> Dict[str, Dict[str, Any]]:
    """
    获取对象方法的详细信息
    
    参数:
        obj: 要检查的Python对象
        
    返回:
        字典，键为方法名，值为包含方法详细信息的字典
    """
    methods_info = {}
    
    for name, member in inspect.getmembers(obj):
        if inspect.ismethod(member) or inspect.isfunction(member):
            try:
                sig = inspect.signature(member)
                params = []
                for param_name, param in sig.parameters.items():
                    param_info = {
                        'name': param_name,
                        'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                        'default': str(param.default) if param.default != inspect.Parameter.empty else 'None',
                        'kind': str(param.kind)
                    }
                    params.append(param_info)
                doc = inspect.getdoc(member)
                if not doc:
                    doc = 'no Docstring.'
                # __init__方法的Docstring含有help信息 唔...... 还是给它去了
                if 'Initialize self.' in doc:
                    doc = 'Initialize self.'
                methods_info[name] = {
                    'name': name,
                    'return_type': str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else 'Any',
                    'parameters': params,
                    'docstring': doc
                }
                
            except (ValueError, TypeError):
                continue
                
    return methods_info

def print_methods_table(methods_info: Dict, title: str = "Methods Information"):
    """
    使用Rich表格打印对象的方法信息
    
    参数:
        methods_info: 字典，为get_methods_info的返回值
        title: 表格标题
    """
    console = Console()

    table = Table(title=title, show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Method", style="cyan", no_wrap=True)
    table.add_column("Return Type", style="green")
    table.add_column("Parameters", style="blue")
    table.add_column("Docstring", style="yellow")

    for method_name, info in methods_info.items():
        param_lines = []
        for param in info['parameters']:
            default_str = f" = {param['default']}" if param['default'] != 'None' else ""
            param_lines.append(
                f"{param['name']}: {param['type']}{default_str} ({param['kind']})"
            )
        param_str = "\n".join(param_lines)
        table.add_row(
            method_name,
            info['return_type'],
            param_str,
            info['docstring']
        )

    console.print(table)
def arg_prase_to_object(arg: str, obj: Any) -> object:
    """
    将用户的输入变为对应的object
    
    参数:
        str arg: 用户的输入
        object obj: 调试的对象
        
    返回:
        tuple output:
            object arg: 对应的object
            bool is_string: 返回值是否为字符串
    """
    if (arg.startswith('"') and arg.endswith('"')) or \
        (arg.startswith("'") and arg.endswith("'")):
        return (arg[1:][:-1], True)
    elif arg.startswith('obj.'):
        try:
            result = eval(arg)
            if isinstance(result, str):
                return (result, True)
            else:
                return (result, False)
        except:
            pass
    else:
        try:
            return (eval(arg), False)
        except NameError:
            print('[!] arg '+ arg + ' undefined. assuming it "' + arg + '"')
            return (str(arg), True)
def format_return(obj: Any) -> str:
    """
    将函数的返回值转化为字符串
    
    参数：
        object obj：返回值
    返回：
        str formatstring：可输出的字符串
    """

    try:
        ret = str(obj)
    except:
        ret = op.objstr(obj)
        if not ret:
            ret = '[Unprintable]'
    return ret
def dbg(obj: Any) -> object:
    """
    调试对象
    
    参数:
        object obj: 要调试的Python对象
        
    返回:
        None: 无返回时返回None
        object obj: 有返回时返回修改后的obj(也可能是未修改的)
    """
    original_obj = deepcopy(obj)
    csle.print(banner, highlight=False)
    check_if_obj_is_builtin = is_builtin(obj)
    if check_if_obj_is_builtin != False:
        return check_if_obj_is_builtin
    csle.print('[*] Details of the object (command "objprint"): \n')
    op(obj, print_methods=True)
    csle.print('')
    while True:
        try:
            cmd = csle.input('[red]objdbg> [/red]')
            if cmd == 'objprint':
                csle.print()
                op(obj, print_methods=True)
                csle.print()
            elif cmd == 'exit' or cmd == 'quit':
                csle.print('[*] Exit with no returns.')
                return None          
            elif cmd == 'retr':
                csle.print('[*] Exit with object returned.')
                return obj
            elif cmd == 'reset':
                csle.print('[*] Reset current object to the original one.')
                obj = deepcopy(original_obj)
            elif cmd == 'pickle':
                csle.print('[*] The pickled data is: '+b64encode(dumps(obj)).decode())
            elif cmd == 'shell':
                try:
                    interact(local=locals())
                except:
                    pass
            elif cmd == 'attr':
                _ = get_object_attributes(obj)
                if _:
                    csle.print_json(data=_)
                elif _ == False:
                    pass
                else:
                    csle.print('[*] Object has no attributes')
            elif cmd == 'help':
                csle.print(banner)
                help = Markdown('''

# commands:

## Static

**objprint**: Lists all attributes & methods of an object. Automatically called each time dbg() is invoked.

**func**: Lists all built-in functions (including overridden magic methods) in the object and their parameters.

**attr**: Lists all attributes of the object.

**pickle**: Outputs pickle.dumps(obj) and encodes it in base64.

**obj.{attr}**: Prints the corresponding attribute of the object.

**dir {obj.xxx}**: Prints dir(obj.xxx). If no argument is provided, defaults to dir(obj).

**func {funcname} {arg1} {arg2} ......**: Calls a function within the object and outputs the return value.

**TODO note**: Quickly lists noteworthy information about the object (e.g., modified magic methods).

......

## Dynamic

**shell**: Switches to the Python interactive shell. The local namespace contains the object being debugged.

**mod_attr** {attrname} {new_value}: Modifies a specific attribute within the object. Supports various nested structures like tuples, lists, and dictionaries.

**reset**: Restores the object in the debugger to its initial state when first passed into the debugger.

**retr**: Stops debugging and returns the object from the debugger.

**exit&quit**: Stops debugging and returns None.

```
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

**del attr {attrname}**: Deletes a specific attribute within the object.

**del func {funcname}**: Disables a specific method in the object.

> Note: Since methods cannot be directly deleted from an instance in Python, when you attempt to del a method, objdbg will set it to None, making it non-callable. However, the attribute itself will not be removed.

**TODO mod_func {funcname} {base64_code}**: Modifies or creates a specific method in the object (pass the code encoded in base64).

''')
                csle.print(help)
            elif cmd.startswith('dir'):
                cmd = cmd.split()
                if len(cmd) == 1:
                    csle.print_json(data=dir(obj))
                elif len(cmd) == 2:
                    obj = eval(cmd[-1])
                    csle.print_json(data=dir(obj))
                    print('[*] ' + cmd[-1] + ' returns ' + format_return(obj) + '. The dir() result is as above.')
                else:
                    csle.print('[-] Parameters error, command format: dir {obj.xxx}')

            elif cmd.startswith('obj.'):
                try:
                    # attr = ''.join(cmd.split('.')[1:])
                    # csle.print('[*] ' + str(getattr(obj, attr)))
                    csle.print(eval(cmd))
                except AttributeError:
                    csle.print('[-] This obj has no attribute {attr}')
            elif cmd.startswith('mod_attr'):
                args = None if len(cmd.split()) < 3 else cmd.split()[1:]
                if args:
                    try:
                        target = args[0]
                        new_value, _ = arg_prase_to_object(''.join(args[1:]), obj)
                        code = 'obj.'+target+'='+str(new_value)
                        setattr(obj, target, new_value)
                        if _:
                            code = 'obj.'+target+'="'+str(new_value) + '"'
                        csle.print('[*] ' + code)
                    except Exception as e:
                        csle.print('[-] An error occurred in modifying attr obj.'+target)
                        csle.print('[-] '+str(e))
                else:
                    csle.print('[-] Parameters error, command format: mod_attr {attrname} {new_value}')
            elif cmd.startswith('del'):
                if cmd.startswith('del attr'):
                    args = None if len(cmd.split()) != 3 else cmd.split()[2:]
                    if args:
                        try:
                            delattr(obj, args[0])
                            csle.print('[*] ' + 'del obj.' + args[0])
                        except Exception as e:
                            csle.print('[-] An error occurred in deleting obj.'+args[0])
                            csle.print('[-] '+str(e))
                    else:
                        csle.print('[-] Parameters error, command format: del attr {attrname}')
                elif cmd.startswith('del func'):
                    args = None if len(cmd.split()) != 3 else cmd.split()[2:]
                    if args:
                        try:
                            setattr(obj, args[0], None)
                            csle.print('[*] ' + 'del obj.' + args[0])
                        except Exception as e:
                            csle.print('[-] An error occurred in deleting obj.'+args[0])
                            csle.print('[-] '+str(e))
                    else:
                        csle.print('[-] Parameters error, command format: del attr {attrname}')
            elif cmd.startswith('func'):
                args = None if len(cmd.split()) == 1 else cmd.split()[1:]
                if args:
                    if not args[0].startswith('obj.'):
                        csle.print('[!] Changing function name from '+args[1] +' to obj.' + args[0])
                        args[0] = 'obj.'+args[0]
                    funcname = args[0]
                    try:
                        func = eval(funcname)
                    except NameError:
                        print('[-] Object has no function ' + '.'.join(funcname.split('.')[1:]))
                        continue
                    if callable(func):
                        args = [arg_prase_to_object(x, obj)[0] for x in args[1:]]
                        try:
                            a = partial(func, *args)()
                            ret = format_return(a)
                            csle.print('[*] Function ' + funcname + ' executed. returned [red][strong]' + ret + '[/red][/strong]')
                        except Exception as e:
                            csle.print('[-] An error occurred when calling func '+funcname + ': ' + str(e))
                    else:
                        csle.print('[-] Attribute '+funcname+' is not callable, type "func" to see all functions in the object')
                else:
                    _ = get_methods_info(obj)
                    if _:
                        print_methods_table(obj)
                    else:
                        csle.print('[*] Object has no functions')
            elif not cmd:
                continue
            else:
                csle.print('[-] no command "' + cmd + '" found. Type "help" for help')
        except KeyboardInterrupt:
            csle.print('\n[*] KeyboardInterrupt detected. Exit with no returns.')
            return None
        except:
            csle.print_exception()
