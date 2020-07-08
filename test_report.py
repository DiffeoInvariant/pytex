from pytex import TestReport, Section, Subsection
import jax
from jax import jit
from jax.numpy import array, eye
from traceback import format_list, extract_stack, print_stack
from sys import exc_info
from abc import ABC


@jax.jit
def sigma(eps):
    return -2.0*eye(3) + eps + eps.T


class TestBaseClass(ABC):
    pass


class TestClass(TestBaseClass):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_a(self):
        # a comment
        return self.a

    def get_b(self):
        """
        a multi-line comment
        """
        return self.b

    def get_c(self):
        return self.c

    


if __name__ == '__main__':

    
    report = TestReport('tests/test_report')
    report.set_title('Test Report')
    report.append(Section('A Section',["Here's some Python code that computes a simple constitutive relation\n",], starred=True))
    report.add_python_function(sigma,'A simple constitutive relation')
    report.append(Section('Test A Class',["Here's a Python class that inherits from an abstract base class.\n",]))
    x = TestClass(1.0,2.0,3.0)
    report.add_python_object(type(x),'A simple Python class')
    output = report.compile().stdout

    buf = 'tests/serialized_report.bin'
    report.serialize(buf)

    print(f"Report: {report}")
    read_report = TestReport.from_file(buf)
    print(f"read-in report: {read_report}")
    
    
    
