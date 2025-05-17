class CustomError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def to_dict(self):
        return {"error": self.message}
