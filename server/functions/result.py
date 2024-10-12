class Result:
    def __init__(self, code = None, msg = None, status = None, body = None):
        self.code = code
        self.msg = msg
        self.status = status
        self.body = body

    def __str__( self ):
        return f'{{"code": "{self.code}", "msg": "{self.msg}", "status": "{self.status}", "body": "{self.body}"}}'
    
    def __repr__( self ):
        return f'{{"code": "{self.code}", "msg": "{self.msg}", "status": "{self.status}", "body": "{self.body}"}}'
