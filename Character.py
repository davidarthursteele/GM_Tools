import math

core_attributes = ["Body","Quickness","Strength","Willpower","Intelligence","Charisma"]
derived_attributes = ["Essence","Reaction","Magic"]

class Character(object):
    def __init__(self, player_name = "Unknown"):
        self.player_name = player_name
        self.character_name  = ""
        self.attributes = self.get_base_attributes()
        self.active_skills = {}
        self.knowledge_skills = {}
        self.language_skills = {}
    def get_base_attributes(self):
        attributes = {}
        for attribute in core_attributes:
            attributes[attribute] = [0,0]
        attributes["Essence"] = [0,0]
        attributes["Magic"] = [0,0]
        attributes["Reaction"] = [0,0]
        attributes["Initiative"]=[0,0]
        return attributes
    
    def refresh_reaction_score(self):
        return int(math.floor((self.attributes["Quickness"][1] + self.attributes["Intelligence"])[1] / 2))
 
    def refresh_magic_score(self):
        return int(math.floor(self.attributes["Essence"]))

    def print_attribute(self, attribute):
        string = ""
        string +=  attribute + (" " * (35 - len(attribute))) + str(self.attributes[attribute][0])
        if self.attributes[attribute][1] != self.attributes[attribute][0]:
            string += "(" + str(self.attributes[attribute][1]) + ")"
        return string
    
    def att_txtstr(self):
        string = "Attributes:\n"
        for att in core_attributes:
            string += "  " + self.print_attribute(att) + "\n"
        for att in derived_attributes:
            if self.attributes[att][0] > 0:
                string += "  " + self.print_attribute(att) + "\n"
        string += "  " + self.print_attribute("Initiative")
        return string
    
    def active_skills_txtstr(self):
        string  = "Active Skills\n"
        for skill in sorted(self.active_skills.keys()):
            string += "  " + skill + (" " * (34 - len(skill))) + " " + self.active_skills[skill][1] + '\n'
        return string
    
    def knowledge_skills_txtstr(self):
        string = "Knowledge Skills\n"
        for skill in sorted(self.knowledge_skills.keys()):
            string += "  " + skill + (" " * (34 - len(skill))) + " " + self.knowledge_skills[skill][1] + "\n"
        return string
    
    def language_skills_txtstr(self):
        string = "Language Skills\n"
        for skill in sorted(self.language_skills.keys()):
            string += "  " + skill + (" " * (34 - len(skill))) + " " + self.language_skills[skill][1] + "\n"
        return string
    
    def export_to_txt(self):
        export = open("characters/"+self.character_name+".txt","w")
        export.write(self.character_name + "\n\n")
        export.write(self.att_txtstr() + "\n\n")     
        export.write(self.active_skills_txtstr()+'\n')
        export.write(self.knowledge_skills_txtstr()+'\n')
        export.write(self.language_skills_txtstr()+'\n')


      
def set_Attributes(char,charinfo):
    for attrib in charinfo["Attributes"]:
        attrib = attrib.split('=')
        if attrib[0] in char.attributes.keys():
            scores = attrib[1].split("|")
            if "(" not in scores[-1]:
                try: char.attributes[attrib[0]] = [int(scores[-1]),int(scores[-1])]
                except: char.attributes[attrib[0]] = [float(scores[-1]),float(scores[-1])]
            else:
                attribscore = scores[-1].rstrip(")").split("(")
                try: char.attributes[attrib[0]] = [int(attribscore[0]),int(attribscore[1])]
                except: char.attributes[attrib[0]] = [float(attribscore[0]),float(attribscore[1])]            
    return char

def get_specced_skill(skill):
    skill1 = [skill[0], skill[1].split(")")[0],skill[2].split('/')[0]]
    skill2 = [skill[0] + " (" +skill[1].split('/')[1]+")", skill[1].split(")")[0],skill[2].split('/')[1]]
    return skill1, skill2

def set_Skills(char,charinfo):
    for skill in charinfo["Skills"]:
        skill = skill.split("=")
        if len(skill) == 3:
            skill = skill[1].split("~")
            skill = [skill[0].split("(")[0],skill[0].split("(")[1].rstrip(")"),(skill[1]).strip("]").strip("[")]
            if "/" in skill[1]:
                skill1, skill2 = get_specced_skill(skill)
                import_skill(char,skill1)
                skill = skill2
            import_skill(char,skill)

def import_skill(char, skill):
    for i in range(len(skill[0])):
        if skill[0][i] == "_":
            skill[0] = skill[0][:i] + " " + skill[0][i+1:]
    if "LAN" in skill[1]:
        if "  " == skill[0][:2]:
            skill[0] = skill[0][2:] + " (R/W)"
        char.language_skills[skill[0]] = ["Intelligence", skill[2]]
    elif "KNO" in skill[1]:
        if ":" in skill[0]:
            skill[0] = (skill[0].split(':')[1]).lstrip(" ")
        char.knowledge_skills[skill[0]] = ["Intelligence", skill[2]]
    else:
        attribute_swap ={"BOD": "Body",
                         "QCK": "Quickness",
                         "STR": "Strength",
                         "INT": "Intelligence",
                         "WIL": "Willpower",
                         "CHA": "Charisma",
                         "REA": "Reaction"}
        char.active_skills[skill[0]] = [attribute_swap[skill[1]], skill[2]]

def set_Cyberware(char, charinfo):
    for ware in charinfo["Cyberware"]:
        try: 
            a = ware.replace("_"," ").split("=")[1].split('~')
            if len(a) > 1: 
                cyberware_name = [a[0],"NA","Standard"]
                if "(A)" in cyberware_name[0]: 
                    cyberware_name[0] = cyberware_name[0][:-3]
                    cyberware_name[2] = "Alphaware"
                if cyberware_name[0][-1] == ']' and cyberware_name[0][-3] == '[':
                    cyberware_name[1] = cyberware_name[0][-2]
                    cyberware_name[0] = cyberware_name[0][:-3]
                if "(CYB)" in cyberware_name[0]:
                    cyberware_name[0] = cyberware_name[0][:-5]
                cyberware_name[0] = cyberware_name[0].rstrip(" ")
                print cyberware_name
        except: pass

def importsr3(filename, player_name = "Unknown"):
    char = Character()
    sr3file = open(filename, 'r')
    charinfo = {}
    for line in sr3file:
        line = line.rstrip('\n').rstrip('\r')
        if len(line) > 0 and line[0] == "[":
            state = line[1:-1]
            charinfo[state] = []
        else:
            if state: charinfo[state].append(line)
    set_Attributes(char,charinfo)
    set_Skills(char,charinfo)
    set_Cyberware(char,charinfo)
    return char


#if __name__ == "__main__":
#    BJ = importsr3("bj.sr3", "BJ")
#    BJ.character_name = "Mecha T"
#    BJ.export_to_txt()