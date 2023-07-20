"""

"""
import sympy


class NodeMapper:
    """
    A class used to map SymPy objects to their corresponding Bifrost nodes.

    ...

    Attributes
    ----------
    node_map : dict
        A dictionary that maps SymPy objects to their bifrost node type counterparts.

    Methods
    -------
    get_mapping(node_name)
        Retrieves the SymPy object associated with a node name.
    """

    def __init__(self):
        """
        Attributes
        ----------
        node_map : dict
            A dictionary that maps SymPy objects tp bifrost node type.
        """
        self.node_map = {
            sympy.core.add.Add: 'Core::Math,add',
            sympy.core.mul.Mul: 'Core::Math,multiply',
            sympy.core.power.Pow: 'Core::Math,power',
            sympy.core.mod.Mod: 'Core::Math,modulo',
            sympy.core.numbers.Integer: 'Core::Constants,float',  # Let's always use floats for now
            sympy.core.numbers.Float: 'Core::Constants,float',
            sympy.core.numbers.Rational: 'Core::Constants,float',
            sympy.core.numbers.Half: 'Core::Constants,float',
            sympy.core.numbers.NegativeOne: 'Core::Constants,float',
            sympy.core.numbers.Zero: 'Core::Constants,float',
            sympy.core.numbers.One: 'Core::Constants,float',
            sympy.core.numbers.Pi: 'Core::Constants,float',
            sympy.functions.elementary.complexes.Abs: 'Core::Math,absolute_value',
            sympy.functions.elementary.exponential.exp: 'Core::Math,exponential',
            sympy.functions.elementary.exponential.log: 'Core::Math,log_base_e',
            sympy.functions.elementary.trigonometric.sin: 'Core::Math,sin',
            sympy.functions.elementary.trigonometric.cos: 'Core::Math,cos',
            sympy.functions.elementary.trigonometric.tan: 'Core::Math,tan',
            sympy.functions.elementary.trigonometric.asin: 'Core::Math,asin',
            sympy.functions.elementary.trigonometric.acos: 'Core::Math,acos',
            sympy.functions.elementary.trigonometric.atan: 'Core::Math,atan',
            sympy.functions.elementary.trigonometric.atan2: 'Core::Math,atan_2D',
            sympy.functions.elementary.hyperbolic.sinh: 'Core::Math,sin_hyperbolic',
            sympy.functions.elementary.hyperbolic.cosh: 'Core::Math,cos_hyperbolic',
            sympy.functions.elementary.hyperbolic.tanh: 'Core::Math,tan_hyperbolic',
            sympy.functions.elementary.hyperbolic.asinh: 'Core::Math,asin_hyperbolic',
            sympy.functions.elementary.hyperbolic.acosh: 'Core::Math,acos_hyperbolic',
            sympy.functions.elementary.hyperbolic.atanh: 'Core::Math,atan_hyperbolic',
            sympy.functions.elementary.miscellaneous.Min: 'Core::Math,min',
            sympy.functions.elementary.miscellaneous.Max: 'Core::Math,max',
            sympy.functions.elementary.integers.ceiling: 'Core::Math,round_to_ceiling',
            sympy.functions.elementary.integers.floor: 'Core::Math,round_to_floor',
            sympy.functions.elementary.miscellaneous.sqrt: 'Core::Math,square_root',
            sympy.functions.elementary.miscellaneous.cbrt: 'Core::Math,cube_root',
        }

        '''
        Add : x + y
        Multiply: x * y
        Power : x**n
        Square root: sqrt(x)
        Cube root: cbrt(x)
        Modulo:  x % y
        Absolute Value: abs(x)
        Exponential (e^x): exp(x)
        Natural Log (log base e): log(x)
        Log (base n): log(x, n)
        Trig functions: sin(x) cos(x) tan(x) asin(x) acos(x) atan(x) atan2(x, y) sinh(x) cosh(x) tanh(x) asinh(x) acosh(x) atanh()
        Minimum: min(*args)
        Maximum: max(*args)
        Round to floor: floor(x)
        Round to ceiling: ceiling(x)
        '''

    def get_mapping(self, sympy_obj):
        """
        Retrieves the bifrost node type associated with a node name.

        Parameters
        ----------
        sympy_obj : class
            The sympy class of the node.

        Returns
        -------
        str
            The bifrost node class associated with the sympy object. If no such node name exists,
            None is returned.
        """
        return self.node_map.get(sympy_obj)
