class AthleteListSBh(list):
    def __init__(self, a_Name, a_Dob, a_Times=[]):
        list.__init__([])
        self.Name  = a_Name
        self.Dob   = a_Dob
        self.extend(a_Times)
    @property
    def top3(self):
        return(sorted(set([sanitize(t) for t in self]))[0:3])

