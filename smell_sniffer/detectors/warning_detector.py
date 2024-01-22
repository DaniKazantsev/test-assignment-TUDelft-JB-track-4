import typing as tp
from otel_trace.trace import Trace
from otel_trace.span import Span

from detectors.issue_detector_base import IssueBase, IssueDetectorBase

class WarningIssue(IssueBase):
    def __init__(self, span, name, warnings):
        super().__init__(span, name)
        self.warnings = warnings

    def __str__(self):
        return f"{self.name} ({self.warnings}) found in {super().__str__()}"

class WarningDetector(IssueDetectorBase):
    def __init__(self, name: str):
        super().__init__(name)

    def check_trace(self, trace: Trace):
        self.check_span(trace.get_main_span)
        return self.issues
        
    def check_span(self, span: Span):
        warnings = span.get('warnings')
        if warnings and len(warnings) > 0:
            for warn in warnings:
                self.issues.append(WarningIssue(span, self.name, warn))
        for child in span.get_children:
            self.check_span(child)