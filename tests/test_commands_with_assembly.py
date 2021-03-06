import filecmp
import sys
import os
import asyncio
import traceback
from asyncio import Task
from typing import List

import pathlib
from aiohttp.web_runner import GracefulExit
from astropy.coordinates import Angle
from termcolor import colored

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.Coords import ProperMotion, EqCoord
from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import Parameter, Struct

class MyComponentHandlers(ComponentHandlers):
    prefix = "CSW.pycswTest"
    commandServer: CommandServer = None
    dir = pathlib.Path(__file__).parent.absolute()
    outFileName = "PyTestAssemblyCommandResponses.out"
    tmpOutFile = f"/tmp/{outFileName}"
    outFile = f"{dir}/{outFileName}"

    def cleanup(self):
        self.showTestResults()
        if os.path.exists(self.tmpOutFile):
            os.remove(self.tmpOutFile)

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(1)
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        print("Long running task completed")
        return Completed(runId)

    # Checks the command's contents, shows how to access the parameters
    # See ./testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#makeTestCommand
    # for where the command was created.
    # noinspection PyUnresolvedReferences
    def _checkCommand(self, command: ControlCommand):
        try:
            assert(command.get("cmdValue").values == [1.0, 2.0, 3.0])
            assert(list(command.get("cmdValue").values)[0] == 1.0)

            # Access a Struct value
            struct: Struct = list(command.get("cmdStructValueB").values)[0]
            # s.__class__ = Struct
            assert(struct.paramSet[0].keyName == "cmdValue")
            assert(struct.paramSet[0].keyType == "FloatKey")
            assert(struct.paramSet[0].values[0] == 1.0)

            # Access a coordinate value
            eqCoord: EqCoord = list(command.get("BasePosition").values)[0]
            assert(eqCoord.pm == ProperMotion(0.5, 2.33))
            assert(eqCoord.ra == Angle("12:13:14.15 hours"))
            assert(eqCoord.dec == Angle("-30:31:32.3 deg"))

        except:
            print(f"_checkCommand: {colored('TEST FAILED', 'red')}")
            traceback.print_exc()

    def showTestResults(self):
        # compare file created by assembly with known good version
        assert filecmp.cmp(self.outFile, self.tmpOutFile, False)
        print(f"{colored('TEST PASSED', 'green')}.")

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component.
        See ./testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#makeTestCommand
        for the contents of the command's parameters.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: (CommandResponse, Task)
            a pair: (subclass of CommandResponse, Task), where the task can be None if the command response is final.
            For long running commands, you can respond with Started(runId, "...") and a task that completes the work in the background.
        """
        self._checkCommand(command)
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        # filt = command.get("filter").values[0]
        # encoder = command.get("encoder").values[0]
        # print(f"filter = {filt}, encoder = {encoder}")

        if command.commandName == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId, "Long running task in progress..."), task
        elif command.commandName == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName == "ResultCommand":
            result = Result([Parameter("myValue", 'DoubleKey', [42.0])])
            return Completed(runId, result), None
        elif command.commandName == "ErrorCommand":
            return Error(runId, "Error command received"), None
        elif command.commandName == "InvalidCommand":
            return Invalid(runId, MissingKeyIssue("Missing required key XXX")), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onOneway method to handle commands from a CSW component.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params.")
        raise GracefulExit()

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        return Accepted(runId)

    # Returns the current state
    def currentStates(self) -> List[CurrentState]:
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")
        return [CurrentState(self.prefix, "PyCswState", [intParam, intArrayParam, floatArrayParam, intMatrixParam])]

def test_command_server():
    handlers = MyComponentHandlers()
    commandServer = CommandServer(handlers.prefix, handlers)
    handlers.commandServer = commandServer
    print(f"Starting test command server on port {commandServer.port}")
    commandServer.start()
    handlers.cleanup()

