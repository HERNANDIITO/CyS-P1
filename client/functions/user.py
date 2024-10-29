
class User:
    def __init__( self, userId: str, privateRSA, publicRSA, aesHash ):
        self.userId     = userId
        self.publicRSA  = privateRSA
        self.privateRSA = publicRSA
        self.aesHash    = aesHash
        
        
    def __str__( self ):
        return f'{{"userId": "{self.userId}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}", "aesHash": "{self.aesHash}"}}'
    
    def __repr__( self ):
        return f'{{"userId": "{self.userId}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}", "aesHash": "{self.aesHash}"}}'
