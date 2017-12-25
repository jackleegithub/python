#利用Python 的 SETUP 工具，安装tickets 脚本
import setuptools
setuptools.setup(
    name='tickets',
    py_modules = ['tickets', 'stations'],
    install_requires = ['requests', 'docopt', 'prettytable'],
    entry_points = {
        'console_scripts':['tickets=tickets.cli']
    }
)
