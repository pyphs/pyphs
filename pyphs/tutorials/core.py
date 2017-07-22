
# import of the pyphs.PHSCore class
from pyphs import Core
import sympy

""" 1) THE RL CORE """

# instantiate a pyphs.Core object
RL= Core(label='my_core')


# Adding the components

xL, L = RL.symbols(['xL', 'L'])    # sympy symbols
HL = xL**2/(2*L)                   # sympy expression
RL.add_storages(xL, HL)            # add a storage component

wR, R = RL.symbols(['wR', 'R'])    # sympy symbols
zR = R*wR                          # sympy expression
RL.add_dissipations(wR, zR)        # add a dissipation component

u1, y1, u2, y2 = RL.symbols(['v1', 'i1', 'v2', 'i2']) #sympy symbols
RL.add_ports([u1, u2], [y1, y2])                      # add the ports

#Initialize the interconnexion matrix
RL.init_M()

# Step by step build of matrix M
RL.set_Mxx([0])
RL.set_Jxw([[-1]])
RL.set_Jxy([[-1, -1]])

#print('Two-ports RL circuit PHS:')
#RL.pprint()

''' 2) THE MKA CORE '''

MKA = Core()

# Define all symbols
xK, K, xM, M, wA, A, u3, v3 = MKA.symbols(['xK', 'K', 'xM', 
'M', 'wA', 'A', 'f3', 'v3'])

# Define the constitutive laws
HK = (xK**2)*(K/2)
HM = (xM**2)/(2*M)
zA = wA*A 

# Add all the components
MKA.add_storages([xK, xM], HK + HM)
MKA.add_dissipations(wA, zA)
MKA.add_ports(u3, v3)

# Initialize the interconnexion matrix
MKA.init_M()

# It is possible to define M at once with a sympy.SparseMatrix
MKA.M = sympy.SparseMatrix([[0, 1, 0, 0], [-1, 0, -1, -1], 
                            [0, 1, 0, 0], [0, 1, 0, 0]])

#print('Mass-spring-damper PHS:')
#MKA.pprint()

""" 3) CONNECTION OF RL AND MKA """

#Additionate both cores 
core = RL + MKA


# Define the symbol BL for the electromechanical connection
BL = core.symbols('BL')

# Add the connector between the port #1 of RL and the port #3 of MKA
core.add_connector((core.y.index(RL.y[1]), core.y.index(MKA.y[0])), alpha = BL)

# Apply the connector
core.connect()

#print('Thiele-Small PHS:')
#core.pprint()

# Reduce the linear dissipative part
core.reduce_z()

#print('z-reduced Thiele-Small PHS:')
#core.pprint()


# Physical parameters 
L_value = 11e-3     #11mH
R_value = 5.7   # 5.7 Ohm
K_value = 4e7 # N/m                         
M_value = 0.019 # 19g
A_value = 0.406 #Ns/m
BL_value = 2.99 #V/A

subs = {L: L_value,
        R: R_value,
        K: K_value, 
        M: M_value,
        A: A_value,
        BL:BL_value
       }

core.subs.update(subs)

# Define the new expression
B = core.symbols('B')
BLnl = B*sympy.exp(-((core.x[1]))**2)

#Associate the expression to BL
core.substitute(subs={BL: BLnl})
core.subs.update({B:BL_value})

# Simplify inversed symbols
core.subsinverse()

# Print the structure
#print('Thiele-Small with nonlinear interconnection PHS:')
#core.pprint()

# Generate the lateX file
#core.texwrite(path=None, title=None, authors=None, affiliations=None)
