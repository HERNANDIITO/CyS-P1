
class User:
    def __init__( self, userId: str, privateRSA, publicRSA ):
        self.userId     = userId
        self.publicRSA  = privateRSA
        self.privateRSA = publicRSA
        
    def __str__( self ):
        return f'{{"userId": "{self.userId}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}"}}'
    
    def __repr__( self ):
        return f'{{"userId": "{self.userId}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}"}}'
