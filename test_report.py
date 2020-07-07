from pytex import TestReport, Section, Subsection
import jax
from jax import jit
from jax.numpy import array, eye
from traceback import format_list, extract_stack, print_stack
from sys import exc_info

@jax.jit
def sigma(eps):
    return -2.0*eye(3) + eps + eps.T


if __name__ == '__main__':

    
    report = TestReport('tests/test_report')
    report.set_title('Test Report')
    report.append(Section('A Section',["Here's some Python code that computes a simple constitutive relation",], starred=True))
    report.add_python_function(sigma,'A simple constitutive relation')
    output = report.compile().stdout

    buf = 'tests/serialized_report.bin'
    report.serialize(buf)

    print(f"Report: {report}")
    read_report = TestReport.from_file(buf)
    print(f"read-in report: {read_report}")
    
    
    
