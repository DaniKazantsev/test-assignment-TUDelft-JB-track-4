import typing as tp
from otel_trace.trace import Trace
from detectors.issue_detector_base import IssueDetectorBase

class MultipleIssueDetector(IssueDetectorBase):
    """
    A composite issue detector that aggregates multiple issue detectors.

    Attributes:
    issue_detectors (List[IssueDetectorBase]): A list of issue detectors that this class will utilize.

    Methods:
    check_traces(traces): Applies all contained issue detectors to each trace in a list of traces.
    check_trace(trace): Applies all contained issue detectors to a single trace.
    """
    def __init__(self, name: str, issue_detectors: tp.List[IssueDetectorBase]):
        super().__init__(name)
        self.issue_detectors = issue_detectors
    
    def check_traces(self, traces: tp.List[Trace]):
        return [self.check_trace(trace) for trace in traces]
   
   
    def check_trace(self, trace: Trace):
        return [detector.check_trace(trace) for detector in self.issue_detectors]
    