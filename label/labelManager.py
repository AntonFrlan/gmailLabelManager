import label.gmail_labels as GL

class labelManager:
    lab = None
    old = None
    def __init__(self):
        lab = []
        f = open("label\\labelNames.txt")
        G = GL.GMailLabelUser()
        s = f.readline()
        dvotocka = False
        vrsta = ""
        lId = ""

        while s:
            rijec = ""

            for i in s:
                if i == ' ' and dvotocka:
                    continue
                elif i == ',':
                    lab.append((vrsta, rijec, lId))
                    rijec = ""
                elif i == ':':
                    vrsta = rijec
                    lId = G.check_labels(vrsta)
                    if "STARO" == vrsta:
                        self.old = lId
                    rijec = ""
                    dvotocka = True
                else:
                    rijec += i

            s = f.readline()

        self.lab = lab
