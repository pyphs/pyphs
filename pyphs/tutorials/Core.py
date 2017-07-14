
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

print('Two-ports RL circuit PHS:')
RL.pprint()

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

print('Mass-spring-damper PHS:')
MKA.pprint()

""" 3) CONNECTION OF RL AND MKA """

#Additionate both cores 
SPK = RL + MKA


# Define the symbol BL for the electromechanical connection
BL = SPK.symbols('BL')

# Add the connector between the port #1 of RL and the port #3 of MKA
SPK.add_connector((SPK.y.index(RL.y[1]), SPK.y.index(MKA.y[0])), alpha = BL)

# Apply the connector
SPK.connect()

print('Thiele-Small PHS:')
SPK.pprint()

# Reduce the linear dissipative part
SPK.reduce_z()

print('z-reduced Thiele-Small PHS:')
SPK.pprint()


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

SPK.subs.update(subs)

# Define the new expression
B = SPK.symbols('B')
BLnl = B*sympy.exp(-((SPK.x[1]))**2)

#Associate the expression to BL
SPK.substitute(subs={BL: BLnl})


# Simplify inversed symbols
SPK.subsinverse()

# Print the structure
print('Thiele-Small with nonlinear interconnection PHS:')
SPK.pprint()

# Generate the lateX file
SPK.texwrite(path=None, title=None, authors=None, affiliations=None)
