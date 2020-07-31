from ufl import *
from fenics import *
from pytex import TestReport, Equation, ufl_form_info



mesh = UnitSquareMesh(10,10)
V = FunctionSpace(mesh,'P',2)
U = VectorFunctionSpace(mesh,'P',2)

u = Function(V)
v = Function(U)

dgu = (dot(v,grad(u)) + div(grad(u))) * dx


report = TestReport('tests/test_ufl',author='Zane Jakobs',use_date=True)
report.set_title('Some UFL Code')
report.append(ufl_form_info(dgu))
report.append(Equation.from_ufl(dgu))
report.write()
report.compile()










