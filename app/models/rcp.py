class Requirement:
    def __init__(self,  name: str, quantity: int, req_id : int, description: str = ""):
        self.name : str = name
        self.quantity : int = quantity
        self.description : str = description
        self.req_id : int = req_id

class Ci:
    def __init__(self, name : str, requirement : list[Requirement], ci_id :int, description : str = ""):
        self.name : str = name
        self.requirements : list[Requirement] = requirement
        self.ci_id : int = ci_id
        self.description : str = description

    def reset_ci(self):
        self.name : str = "Nouveau CI"
        self.requirements : list[Requirement] = []
        self.ci_id : int = 0
        self.description : str = "Description du CI"


requirement1 = Requirement("req1", 100, 1)
requirement2 = Requirement("req2", 200, 2)
requirement3 = Requirement("req3", 300, 3)
requirement4 = Requirement("req4", 400, 4)
requirement5 = Requirement("req5", 100, 5)
requirement6 = Requirement("req6", 200, 6)
requirement7 = Requirement("req7", 300, 7)
requirement8 = Requirement("req8", 400, 8)

requirement_set = {requirement1, requirement2, requirement3, requirement4, requirement5, requirement6, requirement7, requirement8}

ci10 = Ci("Ci10", [requirement1, requirement2], 10, "CI numéro 10")
ci20 = Ci("Ci20", [requirement1, requirement2, requirement3], 20, "CI numéro 20")
ci30 = Ci("Ci30", [requirement5, requirement6], 30, "CI numéro 30")
ci40 = Ci("Ci30", [requirement6, requirement7, requirement8], 40, "CI numéro 40")



ci_set = {ci10, ci20, ci30, ci40}