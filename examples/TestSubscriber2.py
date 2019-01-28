import sys
import os
sys.path.append(os.path.relpath(".."))

from csw_event.EventSubscriber import EventSubscriber

# Test subscribing to events using the wrapper classes
class TestSubscriber2:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribeSystemEvent([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.name}: {i.items}")
        if (systemEvent.isInvalid()):
            print("    Invalid")
        if (systemEvent.exists("assemblyEventValue")):
            p = systemEvent.get("assemblyEventValue")
            if (p != None):
                print(f"Found: {p.name}")


def main():
    TestSubscriber2()

if __name__ == "__main__":
    main()

