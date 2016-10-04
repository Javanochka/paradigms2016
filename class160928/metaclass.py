import re

class MyMetaClass(type):
    def __new__(cls, name, bases, dct):
        compiled_attr = dict((name, re.compile(value)) if name == "regex" else (name, value) for name, value in dct.items())
        return super().__new__(cls, name, bases, compiled_attr)
