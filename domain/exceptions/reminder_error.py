class ReminderError(Exception):

    @property
    def code(self) -> int:
        return  self.args[0]

    @property
    def message(self) -> str:
        return self.args[1]

    def __init__(self, code: int, message: str) -> None:
        super().__init__(code, message)
