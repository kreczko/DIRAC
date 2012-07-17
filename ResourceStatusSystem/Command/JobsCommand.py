# $HeadURL:  $
''' JobsCommand
 
  The Jobs_Command class is a command class to know about 
  present jobs efficiency
  
'''

from DIRAC                                           import gLogger, S_OK, S_ERROR
from DIRAC.ResourceStatusSystem.Command.Command      import Command
#from DIRAC.ResourceStatusSystem.Command.knownAPIs    import initAPIs
#from DIRAC.ResourceStatusSystem.Utilities.Utils      import where
from DIRAC.ResourceStatusSystem.Client.JobsClient import JobsClient
from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient import ResourceStatusClient
from DIRAC.ResourceStatusSystem.Client.ResourceManagementClient import ResourceManagementClient


__RCSID__ = '$Id:  $'

################################################################################
################################################################################

class JobsStatsCommand( Command ):
  
#  __APIs__ = [ 'JobsClient' ]

  def __init__( self, args = None, clients = None ):
    
    super( JobsStatsCommand, self ).__init__( args, clients )
    
    if 'JobsClient' in self.APIs:
      self.jClient = self.APIs[ 'JobsClient' ]
    else:
      self.jClient = JobsClient()  
  
  def doCommand(self):
    """ 
    Return getJobStats from Jobs Client  
    
   :attr:`args`: 
     - args[0]: string: should be a ValidElement

     - args[1]: string: should be the name of the ValidElement

  returns:
    {
      'MeanProcessedJobs': X
    }
    """

#    super(JobsStats_Command, self).doCommand()
#    self.APIs = initAPIs( self.__APIs__, self.APIs )
      
#    try:

    res = self.jClient.getJobsStats( self.args[0], self.args[1], self.args[2] )
      
#    except Exception, e:
#      _msg = '%s (%s): %s' % ( self.__class__.__name__, self.args, e )
#      gLogger.exception( _msg )
#      return S_ERROR( _msg )

    return S_OK( res )   

#  doCommand.__doc__ = Command.doCommand.__doc__ + doCommand.__doc__
    
################################################################################
################################################################################

class JobsEffCommand( Command ):

#  __APIs__ = [ 'JobsClient' ]  

  def __init__( self, args = None, clients = None ):
    
    super( JobsEffCommand, self ).__init__( args, clients )
    
    if 'JobsClient' in self.APIs:
      self.jClient = self.APIs[ 'JobsClient' ]
    else:
      self.jClient = JobsClient()  
  
  def doCommand( self ):
    """ 
    Return getJobsEff from Jobs Client  
    
   :attr:`args`: 
       - args[0]: string: should be a ValidElement
  
       - args[1]: string: should be the name of the ValidElement

    returns:
      {
        'JobsEff': X
      }
    """
    
#    super(JobsEff_Command, self).doCommand()
#    self.APIs = initAPIs( self.__APIs__, self.APIs )    

#    try:
      
    res = self.jClient.getJobsEff( self.args[0], self.args[1], self.args[2] )
       
#    except Exception, e:
#      _msg = '%s (%s): %s' % ( self.__class__.__name__, self.args, e )
#      gLogger.exception( _msg )
#      return S_ERROR( _msg )

    return S_OK( res )   

################################################################################
################################################################################

class SystemChargeCommand( Command ):
  
#  __APIs__ = [ 'JobsClient' ]

  def __init__( self, args = None, clients = None ):
    
    super( SystemChargeCommand, self ).__init__( args, clients )
    
    if 'JobsClient' in self.APIs:
      self.jClient = self.APIs[ 'JobsClient' ]
    else:
      self.jClient = JobsClient()  
  
  def doCommand(self):
    """ Returns last hour system charge, and the system charge of an hour before

        returns:
          {
            'LastHour': n_lastHour
            'anHourBefore': n_anHourBefore
          }
    """
    
#    super(SystemCharge_Command, self).doCommand()
#    self.APIs = initAPIs( self.__APIs__, self.APIs ) 
     
#    try:
      
    res = self.jClient.getSystemCharge()
       
#    except Exception, e:
#      _msg = '%s (%s): %s' % ( self.__class__.__name__, self.args, e )
#      gLogger.exception( _msg )
#      return S_ERROR( _msg )

    return S_OK( res )   
       
#  doCommand.__doc__ = Command.doCommand.__doc__ + doCommand.__doc__
    
################################################################################
################################################################################

class JobsEffSimpleCommand( Command ):
  
#  __APIs__ = [ 'ResourceStatusClient', 'JobsClient' ]

  def __init__( self, args = None, clients = None ):
    
    super( JobsEffSimpleCommand, self ).__init__( args, clients )
    
    if 'JobsClient' in self.APIs:
      self.jClient = self.APIs[ 'JobsClient' ]
    else:
      self.jClient = JobsClient()  
      
    if 'ResourceStatusClient' in self.APIs:
      self.rsClient = self.APIs[ 'ResourceStatusClient' ]
    else:
      self.rsClient = ResourceStatusClient()  
  
  def doCommand( self ):
    """ 
    Returns simple jobs efficiency

    :attr:`args`: 
       - args[0]: string: should be a ValidElement
  
       - args[1]: string should be the name of the ValidElement

    returns:
      {
        'Result': 'Good'|'Fair'|'Poor'|'Idle'|'Bad'
      }
    """
    
#    super (JobsEffSimple_Command, self).doCommand()
#    self.APIs = initAPIs( self.__APIs__, self.APIs )

#    try:
    
    if self.args[0] == 'Service':
      name = self.rsClient.getGeneralName( self.args[0], self.args[1], 'Site' )    
      name        = name[ 'Value' ][ 0 ]
      granularity = 'Site'
    elif self.args[0] == 'Site':
      name        = self.args[1]
      granularity = self.args[0]
    else:
      return S_ERROR( '%s is not a valid granularity' % self.args[ 0 ] )
         
    res = self.jClient.getJobsSimpleEff( name )
     
    if res == None:
      res = S_OK( 'Idle' )
    else:
      res = S_OK( res[ name ] ) 
    
#    except Exception, e:
#      _msg = '%s (%s): %s' % ( self.__class__.__name__, self.args, e )
#      gLogger.exception( _msg )
#      return S_ERROR( _msg )

    return res

#  doCommand.__doc__ = Command.doCommand.__doc__ + doCommand.__doc__
    
################################################################################
################################################################################

class JobsEffSimpleCachedCommand( Command ):
  
#  __APIs__ = [ 'ResourceStatusClient', 'ResourceManagementClient' ]

  def __init__( self, args = None, clients = None ):
    
    super( JobsEffSimpleCachedCommand, self ).__init__( args, clients )
          
    if 'ResourceStatusClient' in self.APIs:
      self.rsClient = self.APIs[ 'ResourceStatusClient' ]
    else:
      self.rsClient = ResourceStatusClient()  
  
    if 'ResourceManagementClient' in self.APIs:
      self.rmClient = self.APIs[ 'ResourceManagementClient' ]
    else:
      self.rmClient = ResourceManagementClient()   
  
  def doCommand( self ):
    """ 
    Returns simple jobs efficiency

    :attr:`args`: 
       - args[0]: string: should be a ValidElement
  
       - args[1]: string should be the name of the ValidElement

    returns:
      {
        'Result': 'Good'|'Fair'|'Poor'|'Idle'|'Bad'
      }
    """
    
#    super(JobsEffSimpleCached_Command, self).doCommand()
#    self.APIs = initAPIs( self.__APIs__, self.APIs )
      
#    try:  
      
    if self.args[0] == 'Service':
      name = self.rsClient.getGeneralName( self.args[0], self.args[1], 'Site' )
      name        = name[ 'Value' ][ 0 ]
      granularity = 'Site'
    elif self.args[0] == 'Site':
      name        = self.args[1]
      granularity = self.args[0]
    else:
      return S_ERROR( '%s is not a valid granularity' % self.args[ 0 ] )
     
    clientDict = { 
                  'name'        : name,
                  'commandName' : 'JobsEffSimpleEveryOne',
                  'value'       : 'JE_S',
                  'opt_ID'      : 'NULL',
                  'meta'        : { 'columns'     : 'Result' }
                  }
      
    res = self.rmClient.getClientCache( **clientDict )
      
    if res[ 'OK' ]:
      res = res[ 'Value' ]
      if res == None or res == []:
        res = S_OK( 'Idle' )
      else:
        res = S_OK( res[ 0 ] )
        
#    except Exception, e:
#      _msg = '%s (%s): %s' % ( self.__class__.__name__, self.args, e )
#      gLogger.exception( _msg )
#      return S_ERROR( _msg )

    return res

#  doCommand.__doc__ = Command.doCommand.__doc__ + doCommand.__doc__
    
################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF