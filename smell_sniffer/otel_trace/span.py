import typing as tp

class Span:
    """
    Represents a single span within a trace.

    Attributes:
    span_data (Dict): The data of the span.
    children (List[Dict]): A list of child spans.
    """
    def __init__(self, spans: tp.Dict[str, tp.Dict], span_name: str, child_by_parent: tp.Dict[str, tp.List[str]]):
        """
        Initialize a Span object with its data and children recoursivly.

        Args:
        spans (Dict[str, Dict]): A dictionary of all spans.
        span_name (str): The name of the current span.
        child_by_parent (Dict[str, List[str]]): A dictionary mapping parent span names to their children's ids.
        """
        self.span_data = spans.get(span_name, {})
        self.children = [Span(spans, child_id, child_by_parent) for child_id in child_by_parent.get(span_name, [])]

    @property
    def get_children(self):
        return self.children

    @property
    def get_data(self):
        return self.span_data

    def get(self, key: str):
        """
        Args:
        key (str): The key for the value to be tried to find.

        Returns:
        The value corresponding to the given key, or None if the key is not found.
        """
        if key not in self.span_data:
            return None
        return self.span_data[key]

    def has_key_in_tags(self):
        """
        Check if the first tag in the span data contains the 'key' field.

        Returns:
        bool: True if the 'key' field is present in the first tag, False otherwise.
        """
        if ('tags' not in self.span_data.keys()
            or len(self.span_data['tags']) == 0  
            or ('key' not in self.span_data['tags'][0].keys())
            ):
            return False
        return True
    
    def has_key_value_in_tags(self, value: str) -> tp.Optional[int]:
        """Get the position of value.

        Args:
            value (str): value

        Returns:
            tp.Optional[tp.Dict]: position or None
        """
        if ('tags' not in self.span_data.keys()
            or len(self.span_data['tags']) == 0):
            return None
        for tag in self.span_data['tags']:
            if 'key' not in tag:
                continue
            if tag['key'] == value:
                return tag
        return None

    def is_tags_key_eq_to_statment(self, statment: str) -> bool:
        """
        Check if the 'key' field in the first tag of the span data equals the given statement.

        Args:
        statement (str): The statement to compare against the 'key' field.

        Returns:
        bool: True if the 'key' field equals the statement, False otherwise.
        """
        if (not self.has_key_in_tags()):
            return False
        return self.span_data['tags'][0]['key'] == statment
    
    
    