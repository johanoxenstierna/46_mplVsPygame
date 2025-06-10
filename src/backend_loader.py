

import P

if P.MPL0PYGAME1 == 0:
    from src.a_mpl.abstract_mpl import AbstractMPLObject as AbstractBackendObject
else:
    from src.a_pygame.abstract_pygame import AbstractPygameObject as AbstractBackendObject
