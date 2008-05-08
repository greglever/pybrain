__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import reshape, dot, outer

from connection import Connection
from pybrain.utilities import substitute
from pybrain.structure.parametercontainer import ParameterContainer

        
class FullConnection(Connection, ParameterContainer):
    """ a connection which fully connects every element from the first module's output buffer
    to the second module's input buffer """
    
    def __init__(self, *args, **kwargs):
        Connection.__init__(self, *args, **kwargs)
        ParameterContainer.__init__(self, self.indim*self.outdim)
    
    @substitute('pybrain.pyrex._full.FullConnection_forwardImplementation')
    def _forwardImplementation(self, inbuf, outbuf):
        outbuf += dot(reshape(self.params, (self.outdim, self.indim)), inbuf)
    
    @substitute('pybrain.pyrex._full.FullConnection_backwardImplementation')
    def _backwardImplementation(self, outerr, inerr, inbuf):
        inerr += dot(reshape(self.params, (self.outdim, self.indim)).T, outerr)
        ds = self.derivs
        ds += outer(inbuf, outerr).T.flatten()                
        
    def whichBuffers(self, paramIndex):
        """ returns the index of the input module's output buffer, and
        the output module's input buffer, for the given weight.  """
        return paramIndex % self.inmod.outdim, paramIndex / self.inmod.outdim
    
    @substitute('pybrain.pyrex._full.FullConnectionforward')
    def forward(self, time, desttime = None):
        Connection.forward(self, time, desttime)
    
    @substitute('pybrain.pyrex._full.FullConnectionbackward')
    def backward(self, time, desttime = None):
        Connection.backward(self, time, desttime)
    