import sys
import os
sys.path.append(os.path.relpath(".."))

from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_event.EventPublisher import EventPublisher

# Test publishing events using the Parameter and SystemEvent wrapper classes
class TestPublisher2:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1,2,3,4], [5,6,7,8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey", [[[1,2,3,4], [5,6,7,8]],[[-1,-2,-3,-4], [-5,-6,-7,-8]]], "meter")
        event = SystemEvent("test.assembly", "myAssemblyEvent", [intParam, intArrayParam, floatArrayParam, intMatrixParam])
        self.pub.publish(event)

def main():
    TestPublisher2()

if __name__ == "__main__":
    main()

