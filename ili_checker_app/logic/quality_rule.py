from ili_checker_app.config.general_config import QR_NAME, QR_DESCRIPTION, QR_RESULT, QR_ERROR


class QualityRule:
    """
        This class return objects with fild name, description, result
    """
    def __init__(self, name: str, description: str, result: int, error: bool = False):
        self._name = name
        self._description = description
        self._result = result
        self._error = error

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def result(self):
        return self._result

    def return_dict(self) -> dict:
        return {
            QR_NAME: self._name,
            QR_DESCRIPTION: self._description,
            QR_RESULT: self._result,
            QR_ERROR: self._error if self._error else None
        }
