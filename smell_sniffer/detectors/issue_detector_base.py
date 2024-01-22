import typing as tp
from trace import Trace

class IssueBase:
    """
    Represents a basic structure of an issue.

    Attributes:
    span_id (str): The ID of the span where the issue was identified.
    trace_id (str): The ID of the trace that the span belongs to.
    operation_name (str): The operation name associated with the span.
    name (str): The name of the issue.
    """
    def __init__(self, span, name):
        self.span_id = span.get('spanID')
        self.trace_id = span.get('traceID')
        self.operation_name = span.get('operationName')
        self.name = name
        
    def __str__(self):
        return f"span_id: {self.span_id}, trace_id: {self.trace_id}, operation_name: {self.operation_name}"

class IssueDetectorBase:
    """
    Base class for issues detector in traces.

    Attributes:
    name (str): The name of the issue detector.
    issues (List[IssueBase]): A list of detected issues.
    """
    def __init__(self, name: str):
        self.name = name
        self.issues = []
    
    def check_traces(self, traces: tp.List[Trace]) -> tp.List[IssueBase]:
        return [self.check_trace(trace) for trace in traces]
    
    @property
    def get_issues(self):
        return self.issues