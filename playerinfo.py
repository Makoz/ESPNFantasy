class PlayerInfo():

    def __init__(self, pId):
        self.Id = pId
        self.teamMembers = []
    
    def addPlayer(self, player):
        self.teamMembers.append(player)

    def removePlayer(self, player):
        self.teamMembers.remove(player)

