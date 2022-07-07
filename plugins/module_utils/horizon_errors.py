class HorizonError(Exception):
    def __init__(self, code, message, response, detail=None):
        self.code = code
        self.message = message
        self.detail = detail
        self.response = response

        full_message = "Error %s : %s" % (self.code, self.message)
        if self.detail:
            full_message = "%s (%s)" % (full_message, self.detail)

        super().__init__(full_message)