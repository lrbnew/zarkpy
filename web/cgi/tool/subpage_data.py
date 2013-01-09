#coding=utf-8
# 为subpage模版提供数据，有时通过传参的形式向模版文件传递数据并不方便
# 那么可以考虑在此文件中添加一个新的函数，然后在模版中直接通过$subpage_data.functionName()的方式返回数据, 详见app.py中对subpage_data的引用
