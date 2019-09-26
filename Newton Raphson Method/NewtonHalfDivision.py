from sympy import diff, S, lambdify, symbols, pi
from numpy import float64, seterr
from mpmath import pi

class TEST:
    pass

class Root(object):
    def __init__(self, SegIn1):
        self.intermediate_root = SegIn1
        self.final_root = None
class FuntuionPropreties(object):
    x = symbols('x', real = True)
    def __init__(self, Func1):
        self.objective_funtuion = S(Func1).replace('x', FuntuionPropreties.x)
        self.first_derivative = diff(self.objective_funtuion, FuntuionPropreties.x)
        self.second_derivative = diff(self.objective_funtuion, FuntuionPropreties.x, 2)
        self.first_delta_function = lambdify(FuntuionPropreties.x, self.first_derivative)
        self.second_delta_function = lambdify(FuntuionPropreties.x, self.second_derivative)
        self.lambda_function = lambdify(FuntuionPropreties.x, self.objective_funtuion, "numpy")
    def __str__(self):
        return "Function: " + str(self.function)
class Segments(Root):
    def __init__(self, SegIn1, SegOut1, NumOfSeg):
        Root.__init__(self, SegIn1)
        self.right_side = SegOut1
        self.left_side = SegIn1
        self.number_segments = NumOfSeg
class TaskOptions(FuntuionPropreties, Segments):
    def __init__(self, e, SegIn1, SegOut1, Count, NumOfSeg, Func1):
        FuntuionPropreties.__init__(self, Func1)
        Segments.__init__(self, SegIn1, SegOut1, NumOfSeg)
        self.epsilon = e
        self.number_iterations = Count
    def first_step(self):
        return (self.intermediate_root - (self.lambda_function(self.intermediate_root))/
            float64((self.first_delta_function(self.intermediate_root))))
    def __str__(self):
        return "Objective Function:" + str(self.objective_funtuion)
def NewtonHalfDivision(IN):
    OUT = TEST()
    if hasattr(IN, 'Count'):
       pass
    else:
        IN.Count = 100
    if hasattr(IN, 'NumOfSeg'):
       pass
    else:
        IN.NumOfSeg = 100
    if hasattr(IN, 'SegOut1'):
       pass
    else:
        IN.SegOut1 = float('inf')
    task = TaskOptions(IN.e, IN.SegIn1, IN.SegOut1, IN.Count, IN.NumOfSeg, IN.Func1)

    seterr(all='raise')
    flag_check = 0

    while flag_check != 1:
        try:
            x_check = task.lambda_function(task.left_side)
        except FloatingPointError, e:
                if e.args[0] == ('invalid value encountered in log'):
                    task.left_side = task.left_side + (abs(task.left_side) + abs(task.right_side)) / float(task.number_segments)
                    continue
                else:
                    print "ERROR: ", e.args
        except ValueError, e:
            if e.args[0] == ('negative number cannot be raised to a fractional power'):
                task.left_side = 0
            else:
                print "ERROR: ", e.args
        flag_check = 1

    seterr(all='ignore')
    if task.right_side < task.left_side:
        buff = task.left_side
        task.left_side = task.right_side
        task.right_side = buff

    long = (abs(task.left_side) + abs(task.right_side)) / float(task.number_segments)
    for i in range(0, task.number_segments):
        task.right_side = task.left_side + long
        task.intermediate_root = task.left_side

        if float64(task.epsilon) >= abs(task.intermediate_root):
            if float64(task.epsilon) >= abs(task.lambda_function(task.intermediate_root)):
                OUT.VecOut1 = task.intermediate_root
                return OUT
            elif float64(task.epsilon) >= abs(task.lambda_function(1)):
                OUT.VecOut1 = 1
                return OUT
            elif float64(task.epsilon) >= abs(task.lambda_function(float(pi))):
                OUT.VecOut1 = pi
                return OUT 
                
        if task.lambda_function(task.left_side)*task.lambda_function(task.right_side) > 0:
            task.left_side = task.right_side
            continue
            
        if int(task.first_delta_function(IN.SegIn1)) == IN.SegIn1*5:
            task.intermediate_root = (task.left_side + task.right_side) / float(2)
            
        while (task.number_iterations != 0):
            
            task.final_root = task.first_step()
            
            while (abs(task.lambda_function(task.final_root)) > abs(task.first_delta_function(task.intermediate_root))):
                task.final_root = (task.intermediate_root + task.final_root) / float(2)
                if task.number_iterations < 0:
                    break
                task.number_iterations -= 1
            if float64(task.epsilon) >= abs(task.lambda_function(task.final_root)):
                
                if task.final_root == None:
                    OUT.VecOut1 = float('inf')
                elif task.final_root < task.left_side:
                    task.final_root = task.final_root + pi
                    OUT.VecOut1 = task.final_root
                else:
                    OUT.VecOut1 = task.final_root
                return OUT
            else:
                task.number_iterations -= 1
                task.intermediate_root = task.final_root
        task.left_side = task.right_side
    if task.final_root == None:
        if float64(task.epsilon) >= abs(task.lambda_function(0)) and IN.SegIn1 <= 0 and IN.SegOut1 >= 0:
            OUT.VecOut1 = 0
        else:
            
            OUT.VecOut1 = float('inf')
    else:
        OUT.VecOut1 = task.final_root
        
    return OUT
def main():
    IN = [TEST()]

    IN[0].e = 0.0001
    IN[0].SegIn1 = -3
    IN[0].SegOut1 = 5
    IN[0].Func1 = 'x**2'
    IN[0].NumOfSeg = 100

    print (NewtonHalfDivision(IN[0]))
if __name__ == '__main__':
    main()