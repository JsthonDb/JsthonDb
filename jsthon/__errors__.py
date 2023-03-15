class UnknownKeyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class FunctionIsNotCallable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class WrongIdsListWasGiven(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class IdWasNotFound(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class IdIsAlreadyUsed(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class NotUniqueNameOfTable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class WrongFileName(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class WrongTypeOfEncryptedData(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class KeysWereNotGenerated(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
