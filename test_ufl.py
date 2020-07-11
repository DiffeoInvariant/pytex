from ufl import *
from fenics import *
from pytex import TestReport, Equation



mesh = UnitSquareMesh(8,8)
V = FunctionSpace(mesh,'P',1)
U = VectorFunctionSpace(mesh,'P',1)

u = Function(V)

dgu = div(grad(u)) * dx


report = TestReport('tests/test_ufl')
report.set_title('Some UFL Code')
report.append(Equation.from_ufl(dgu))
report.write()
report.compile()










