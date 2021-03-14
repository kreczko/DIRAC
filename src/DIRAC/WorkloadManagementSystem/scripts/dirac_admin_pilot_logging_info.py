#! /usr/bin/env python
"""
Get Pilots Logging for specific Pilot UUID or Job ID.

Usage:
  dirac-admin-pilot-loggin-info <option value>

  WARNING: Only one option (either uuid or jobid) should be used.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
__RCSID__ = "$Id$"

import DIRAC
from DIRAC import S_OK, gLogger
from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript

uuid = None
jobid = None


def setUUID(optVal):
  """
  Set UUID from arguments
  """
  global uuid
  uuid = optVal
  return S_OK()


def setJobID(optVal):
  """
  Set JobID from arguments
  """
  global jobid
  jobid = optVal
  return S_OK()


@DIRACScript()
def main(self):
  global uuid
  global jobid
  self.registerSwitch('u:', 'uuid=', 'get PilotsLogging for given Pilot UUID', setUUID)
  self.registerSwitch('j:', 'jobid=', 'get PilotsLogging for given Job ID', setJobID)
  self.parseCommandLine()

  from DIRAC.WorkloadManagementSystem.Client.PilotManagerClient import PilotManagerClient

  if jobid:
    result = PilotManagerClient().getPilots(jobid)
    if not result['OK']:
      gLogger.error(result['Message'])
      DIRAC.exit(1)
    gLogger.debug(result['Value'])
    uuid = list(result['Value'])[0]

  result = PilotManagerClient().getPilotLoggingInfo(uuid)
  if not result['OK']:
    gLogger.error(result['Message'])
    DIRAC.exit(1)
  gLogger.notice(result['Value'])

  DIRAC.exit(0)


if __name__ == "__main__":
  main()
