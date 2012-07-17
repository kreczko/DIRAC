# $HeadURL:  $
''' VOBOXAvailabilityCommand
  
  The Command pings a service on a vobox.
  
'''

import urlparse

from DIRAC                                      import S_OK, S_ERROR
from DIRAC.Core.DISET.RPCClient                 import RPCClient
from DIRAC.ResourceStatusSystem.Command.Command import Command

__RCSID__ = '$Id:  $'

class VOBOXAvailabilityCommand( Command ):
  '''
  Given an url pointing to a service on a vobox, use DIRAC ping against it.
  ''' 
  
  def doCommand( self ):
    '''
    Run the command.
    '''
    #super( VOBOXAvailabilityCommand, self ).doCommand()
    
    if not 'serviceURL' in self.args:
      return S_ERROR( '"serviceURL" not found in self.args' )
    serviceURL   = self.args[ 'serviceURL' ]
    
    pinger  = RPCClient( serviceURL )
    resPing = pinger.ping()
    
    if not resPing[ 'OK' ]:
      return resPing 
      
    serviceUpTime = resPing[ 'Value' ].get( 'service uptime', 0 )
    machineUpTime = resPing[ 'Value' ].get( 'host uptime', 0 )
      
    parsed          = urlparse.urlparse( serviceURL )
    system, service = parsed.path.strip( '/' ).split( '/' )
    site            = parsed.netloc.split( ':' )[0]
      
    res = { 
           'serviceUpTime' : serviceUpTime,
           'machineUpTime' : machineUpTime,
           'site'          : site,
           'system'        : system,
           'service'       : service
          }       
      
    return S_OK( res )       
    
################################################################################      
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF  