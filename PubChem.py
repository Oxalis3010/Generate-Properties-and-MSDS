class PubChem:
    def __init__(self, page):
        self.page = page
        self.hazard = []
        self.output = []
        self.chemical = ""
        self.molar = ""
        self.CAS = ""
        self.formula = ""
        self.density = ""

    def find(self):
        self.findCAS()
        self.findChemical()
        self.findFormula()
        self.findHazard()
        self.findMolar()
        self.fineDensity()

    def findHazard(self):
        try:
            start = self.page.index("GHS Hazard Statements\t")
            end = self.page.index("Precautionary Statement Codes\t")
            self.hazard.append("Hazard Category:\n")
            for i in range(1, end - start):
                if i % 2 == 0:
                    continue
                self.hazard.append(self.page[start + i] + "\n")
        except ValueError:
            self.hazard.append("Hazard information not found\n")

    def findChemical(self):
        try:
            point = self.page.index("compound Summary")
            self.chemical = self.page[point + 1]
        except ValueError:
            self.chemical = "Chemical name not found"

    def findMolar(self):
        try:
            point = self.page.index("Molecular Weight\t")
            self.molar = "Molecular Weight: " + self.page[point + 1]
        except ValueError:
            self.molar = "Molecular Weight not found"

    def findCAS(self):
        try:
            point = self.page.index("2.3.1 CAS")
            self.CAS = "CAS Number: " + self.page[point + 2]
        except ValueError:
            self.CAS = "CAS Number not found"

    def findFormula(self):
        try:
            point = self.page.index("Molecular Formula\t")
            self.formula = "Chemical Formula: " + self.page[point + 1]
        except ValueError:
            self.formula = "Chemical Formula not found"

    def fineDensity(self):
        try:
            section_point = self.page.index("3.2.9 Density")
            self.density = "Density: " + self.page[section_point + 5]
            if self.density.split(" ").pop(2) != "g/cu":
                self.density = ""
        except ValueError:
            self.density = ""


    def getChemical(self):
        return self.chemical

    def getMolar(self):
        return self.molar

    def getCAS(self):
        return self.CAS

    def getHazard(self):
        return "".join(self.hazard)

    def getFormula(self):
        return self.formula

    def getDensity(self):
        return self.density

    def __str__(self):
        result = []
        result.append(self.getChemical())
        result.append(self.getCAS())
        result.append(self.getFormula())
        result.append(self.getMolar())
        result.append(self.getDensity())
        result.append(self.getHazard())
        return "\n".join(result)
