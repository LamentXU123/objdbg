# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2025/04/30 12:45:40
@Author  :   LamentXU 
'''
from objprint import op
from rich.console import Console 
from rich.table import Table
from code import interact
from types import FunctionType
from pickle import dumps
from copy import deepcopy
from base64 import b64decode, b64encode
from functools import partial
import inspect
from typing import Any, Dict
VERSION = '0.1.1'
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
    
    参数：要检查的Python对象

    返回:
        字典，键为属性名，值为属性内容
    
    """
    return {
        key: value 
        for key, value in vars(obj).items()
        if not callable(value) and not key.startswith('__')
    }

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

def print_methods_table(obj: Any, title: str = "Methods Information"):
    """
    使用Rich表格打印对象的方法信息
    
    参数:
        obj: 要检查的Python对象
        title: 表格标题
    """
    methods_info = get_methods_info(obj)
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
def arg_prase_to_object(arg: str) -> object:
    """
    将用户的输入变为对应的object
    
    参数:
        str arg: 用户的输入
        
    返回:
        object arg: 对应的object
    """
    if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
        return arg
    try:
        return eval(arg)
    except NameError:
        print('[!] arg '+ arg + ' undefined. assuming it "' + arg + '"')
        return '"'+str(arg)+'"'
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
                csle.print_json(data=get_object_attributes(obj))
            elif cmd.startswith('obj.'):
                # csle.print(eval(cmd)) 其实就可以但是我不想 :(
                attr = ''.join(cmd.split('.')[1:])
                try:
                    csle.print('[*] ' + str(getattr(obj, attr)))
                except AttributeError:
                    csle.print(f'[-] This obj has no attribute {attr}')
            elif cmd.startswith('mod_attr'):
                args = None if len(cmd.split()) < 3 else cmd.split()[1:]
                if args:
                    try:
                        target = args[0]
                        new_value = arg_prase_to_object(''.join(args[1:]))
                        code = 'obj.'+target+'='+str(new_value)
                        setattr(obj, target, new_value)
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
                    funcname = args[0]
                    func = getattr(obj, funcname)
                    if callable(func):
                        args = [arg_prase_to_object(x) for x in args[1:]]
                        try:
                            a = partial(func, *args)()
                            try:
                                ret = str(a)
                            except:
                                ret = op.objstr(a)
                            csle.print('Function ' + funcname + ' executed. returned [red][strong]' + ret + '[/red][/strong]')
                        except Exception as e:
                            csle.print('[-] An error occurred when calling func '+funcname + ': ' + str(e))
                    else:
                        csle.print('[-] Attribute '+funcname+' is not callable, type "func" to see all functions in the object')
                else:
                    print_methods_table(obj)
            else:
                csle.print('[-] no command "' + cmd + '" found.')
        except KeyboardInterrupt:
            csle.print('\n[*] KeyboardInterrupt detected. Exit with no returns.')
            return None
        except:
            csle.print_exception()
