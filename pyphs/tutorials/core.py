
# import of the pyphs.PHSCore class
from pyphs import Core
import sympy

# instantiate a pyphs.Core object
spring = Core(label='spring')
# Adding the components
q, k = spring.symbols(['q', 'k'])  # sympy symbols
Hk = k*q**2/2                      # sympy expression
spring.add_storages(q, Hk)         # add a storage component
uk, yk = spring.symbols(['vk', 'fk'])   # sympy symbols
spring.add_ports(uk, yk)                # add the ports
# Step by step build of matrix M
spring.set_Mxx([0])
spring.set_Jxy([[1]])
# spring.pprint()


# instantiate a pyphs.Core object
mass = Core(label='mass')
# Adding the components
p, m = spring.symbols(['p', 'm'])  # sympy symbols
Hm = p**2/(2*m)                      # sympy expression
mass.add_storages(p, Hm)         # add a storage component
um, ym = mass.symbols(['fm', 'vm'])   # sympy symbols
mass.add_ports(um, ym)                # add the ports
# Step by step build of matrix M
mass.set_Mxx([0])
mass.set_Jxy([[-1]])
# mass.pprint()

massspring = mass + spring
# massspring.pprint()

massspring.add_connector((0, 1))
massspring.connect()
# massspring.pprint()

w, a = massspring.symbols(['w', 'a'])  # sympy symbols
z = a*w                            # sympy expression
massspring.add_dissipations(w, z)  # add a storage component
# massspring.pprint()

massspring.set_Jxw([[-1.0], [0.0]])
# massspring.pprint()

massspring.reduce_z()
# massspring.pprint()


core = massspring.__copy__()
core.H += (k/10)*q**4/4
u, y = core.symbols(['fin', 'vout'])    # sympy symbols
core.add_ports(u, y)                    # add the ports
core.set_Jxy([[-1.0], [0.0]])           # define gain
core.move_storage(0,1)
# core.pprint()


core.subs = {m: 0.01,
             k: 4e3,
             a: 0.1}
