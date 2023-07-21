# exprToCompound

Takes a mathematical expression and converts it into a Bifrost compound. Launch the tool with the `exprToCompound` MEL command and enter your expression using python syntax. 

## Available operators

Add : `x + y`  
Multiply: `x * y`  
Power : `x**n`  
Square root: `sqrt(x)`  
Cube root: `cbrt(x)`  
Modulo:  `x % y`  
Absolute Value: `abs(x)`  
Exponential (e^x): `exp(x)`  
Natural Log (log base e): `log(x)`  
Log (base n): `log(x, n)`  
Trig functions: `sin(x)` `cos(x)` `tan(x)` `asin(x)` `acos(x)` `atan(x)` `atan2(x, y)` `sinh(x)` `cosh(x)` `tanh(x)` `asinh(x)` `acosh(x)` `atanh()`  
Minimum: `min(*args)` (e.g. `min(x, y, z)`)  
Maximum: `max(*args)` (e.g. `max(x, y, z)`)    
Round to floor: `floor(x)`  
Round to ceiling: `ceiling(x)`  

_note: You can name variables how you'd like the ports named on your node, so if you enter `a*sin(theta)` your node will end up with a port named `a` and a port named `theta`_
