import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    """JSON encoder that handles NumPy scalar and array types.

    Converts ``np.integer`` → ``int``, ``np.floating`` → ``float``, and
    ``np.ndarray`` → ``list`` so that NumPy values can be serialised with
    ``json.dumps``.
    """

    def default(self, obj):
        """Serialise NumPy types; fall back to the base encoder for others.

        Args:
            obj: Object to serialise.

        Returns:
            A JSON-serialisable Python built-in type.
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)