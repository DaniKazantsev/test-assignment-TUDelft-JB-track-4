import typing as tp
from otel_trace.trace import Trace
from otel_trace.span import Span

from detectors.issue_detector_base import IssueBase, IssueDetectorBase

ERROR_TAG = {
    "key": "error",
    "type": "bool",
    "value": True
}

class HTTPErrorIssue(IssueBase):
    """
    Represents an issue identified as an http error within a span.
    """
    def __init__(self, span, name):
        super().__init__(span, name)


    def __str__(self):
        return f"{self.name} found in {super().__str__()}"

class HTTPErrorDetector(IssueDetectorBase):
    """
    Detector class for identifying http errors in traces.

    Methods:
    check_trace(trace): Checks a single trace for exception issues.
    check_span(span): Recursively checks a span and its children for http errors.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def check_trace(self, trace: Trace):
        self.check_span(trace.get_main_span)
        return self.issues
        
    def check_span(self, span: Span):
        position_in_tags = span.has_key_value_in_tags("error")

        if position_in_tags and position_in_tags == ERROR_TAG and span.get('tags')[0]['key'] == "http.scheme":
                self.issues.append(HTTPErrorIssue(span, self.name))
        for child in span.get_children:
            self.check_span(child)