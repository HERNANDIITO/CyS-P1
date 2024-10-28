
class User:
    def __init__( self, userId: str, privateRSA, publicRSA ):
        self.userId     = userId
        self.publicRSA  = privateRSA
        self.privateRSA = publicRSA