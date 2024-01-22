import typing as tp
from otel_trace.trace import Trace
from otel_trace.span import Span

from detectors.issue_detector_base import IssueBase, IssueDetectorBase

EXCEPTION_LOG = {
    "key": "event",
    "type": "string",
    "value": "exception"
}


class ExceptionIssue(IssueBase):
    """
    Represents an issue identified as an exception within a span.

    Attributes:
    message (str): The exception message.
    """
    def __init__(self, span, name, message):
        super().__init__(span, name)
        self.message = message

    def __str__(self):
        return f"{self.name} ({self.message}) found in {super().__str__()}"

class ExceptionDetector(IssueDetectorBase):
    """
    Detector class for identifying exceptions in traces.

    Methods:
    check_trace(trace): Checks a single trace for exception issues.
    check_span(span): Recursively checks a span and its children for exception logs.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def check_trace(self, trace: Trace):
        self.check_span(trace.get_main_span)
        return self.issues
        
    def check_span(self, span: Span):
        logs = span.get('logs')
        if logs:
            for log in logs:
                for field in log['fields']:
                    if (field == EXCEPTION_LOG):
                        for message_field in log['fields']:
                            if message_field['key'] == 'exception.message':
                                self.issues.append(ExceptionIssue(span, self.name, message_field['value']))
        for child in span.get_children:
            self.check_span(child)