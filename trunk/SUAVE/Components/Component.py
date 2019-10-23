## @ingroup Components
# Component.py
# 
# Created:  
# Modified: Dec 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Data
from SUAVE.Core import Container as ContainerBase
import numpy as np

# ----------------------------------------------------------------------
#  Component
# ----------------------------------------------------------------------

## @ingroup Components
class Component(Data):
    """ the base component class
        Assumptions:
        None
        
        Source:
        None
    """
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
            """         
        self.tag        = 'Component'
        self.origin     = [[0.0,0.0,0.0]]
        self.materials  = ContainerBase()

    
# ----------------------------------------------------------------------
#  Component Container
# ----------------------------------------------------------------------

## @ingroup Components
class Container(ContainerBase):
    """ the base component container class
    
        Assumptions:
        None
        
        Source:
        None
    """
    pass


# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Component.Container = Container