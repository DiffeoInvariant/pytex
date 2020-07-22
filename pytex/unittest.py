import unittest
from pickle import dump,load
from os import makedirs
from os.path import abspath, exists, dirname
from typing import Dict, Tuple, Sequence
from collections.abc import Iterable
from inspect import getmembers, ismethod


class TestResultGenerator:

    def __init__(self, funcs, args, results_dir):
        self._check_directory(results_dir)
        self.directory = results_dir
        self.funcs_and_args = self._get_functions_and_args(funcs,args)



    def write_results(self):
        for f, args in self.funcs_and_args:
            fn = self._get_file_name(f)
            res = f(*args)
            dump(res,open(fn,'wb'))


    def _get_file_name(self, func): 
        return self.directory + '/test_' + func.__name__ + '.dat'
        
        
    def _check_directory(self, resdir):
        dr = dirname(abspath(resdir))
        if not exists(dr):
            makedirs(dr)

    def _get_functions_and_args(self, funcs, args):
        if callable(funcs):
            return [(funcs,args)]
            
        elif isinstance(funcs,Iterable):
            if not isinstance(args,Iterable) or (len(args) != len(funcs)):
                raise RuntimeError("Error, must pass same number of functions (passed {len(funcs)}) and argument tuples (passed {len(args) if isinstance(args,Iterable) else 1}) to TestResultGenerator()")

            return zip(funcs,[tuple(x) for x in args])

    
class _DeprecatedTestCase(unittest.TestCase):

    def __init__(self,fname,saved_results):
        self.set_results(saved_results)
        super().__init__(fname)

    """
    Use this class by inheriting from it; if you want to test a function named `foo()`, you would provide a method called `run_foo(self)` (regardless of how many arguments `foo()` takes) and a dictionary mapping the string "foo" to a filename containing a pickled Python object that should compare True to the return value of run_foo

    @arg saved_results: dictionary mapping function base names to tuple of 

((file containing pickled object s.t. operator== compares True with that object and the correct result of the test, False otherwise), (error message to prinf if the comparison comes up False))

(i.e. we pass the test in a function called `run_func(self)` iff our result equals the result loaded from the file saved_results["func"]))
    """
    def set_results(self, saved_results: Dict[str,Tuple[str,str]]):
        self.results = saved_results
        self.runnables = self._get_runnables()
    
        
    def setUp(self):
        try:
            self.expected_results = self._get_saved_results()
        except RuntimeError:
            raise

        self._make_test_functions()
        
    def _get_runnables(self):
        members = getmembers(self,predicate=ismethod)
        runners = set()
        for memtpl in members:
            name, fn = memtpl
            if name.startswith('run_'):
                runners.add('_'.join(name.split('_')[1:]))

        return runners

    def _get_saved_results(self):
        loaded_results = self.results
        for fn in self.runnables:
            if fn in self.results.keys():
                with open(self.results[fn][0],'rb') as fl:
                    loaded_results[fn] = load(fl)
            else:
                raise RuntimeError(f"Could not find expected results file for function {fn}!")

        return loaded_results

    def _make_test_functions(self):
        for func_name_base in self.runnables:
            self._make_test_function(func_name_base)

    def _make_test_function(self, name_base):
        fn = getattr(self, 'run_'+name_base)
        expected_val = self.expected_results[name_base]
        err_msg = self.results[name_base][1]
        def runner(self):
            self.assertEqual(fn(self),expected_val,err_msg)

        testname = 'test_'+name_base
        setattr(self,testname,runner)
                
                

