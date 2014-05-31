##
#### TODO:
##


import Dice

srdice = Dice.shadowrun_dice()
dice = Dice.dice()

class host(object):
    def __init__(self, color = "", difficulty = ""):
        if color == "":
            self.color = self.get_host_color()
        else:
            self.color = color
        if difficulty == "":
            self.difficulty = self.get_difficulty()
        else:
            self.difficulty = difficulty
        self.security_value = self.get_security_value()
        self.subsystems = {"Access": 0, "Control": 0, "Index": 0, "Files": 0, "Slave": 0}
        for subsystem in self.subsystems:
            self.subsystems[subsystem] = self.get_subsystem_rating()
        sheaf_object = security_sheaf(self.color, self.security_value)
        self.sheaf = sheaf_object.sheaf
        paydata_points = self.get_paydata_points()
        self.paydata = []
        for _ in range(paydata_points):
            self.paydata.append((self.get_paydata_size(), self.get_paydata_security()))

    def get_host_color(self):
        hosts = ["Blue","Green","Orange","Red"]
        host_color = raw_input("What Color Security Does the Host Have?  (Blue, Green, Orange, Red) -- ").lower()
        host_color = host_color[0].upper() + host_color[1:]
        while host_color not in hosts:
            print
            print "Please select one of the colors provided."
            print
            host_color = raw_input("What Color Security Does the Host Have?  (Blue, Green, Orange, Red) -- ").lower()
        return host_color
    
    def get_difficulty(self):
        difficulties = ["easy","average","hard"]
        diff = raw_input("How Difficult Should the Host Be? (Easy, Average, Hard) -- ").lower()
        while diff not in difficulties:
            print
            print "Please select a difficulty provided."
            print
            diff = raw_input("How Difficult Should the Host Be? (Easy, Average, Hard) -- ").lower()
        return diff
    
    def get_security_value(self):
        if self.difficulty == "easy":
            return dice.roll_one_die(3) + 3
        elif self.difficulty == "average":
            return dice.roll_one_die(3) + 6
        elif self.difficulty == "hard":
            return sum(dice.roll_multi_dice(2, 3)) + 6
        
    def get_subsystem_rating(self):
        if self.difficulty == "easy":
            return dice.roll_one_die(3) + 7
        elif self.difficulty == "average":
            return dice.roll_one_die(3) + 9
        elif self.difficulty == "hard":
            return dice.roll_one_die(6) + 12

    def get_paydata_points(self):
        if self.color == "Blue":
            return dice.roll_one_die(6) - 1
        elif self.color == "Green":
            return sum(dice.roll_multi_dice(2,6)) - 2
        elif self.color == "Orange":
            return sum(dice.roll_multi_dice(2,6))
        else:
            return sum(dice.roll_multi_dice(2,6)) + 2

    def get_paydata_size(self):
        roll_mod = {"Blue": 20, "Green": 15, "Orange": 10, "Red": 5}
        return sum(dice.roll_multi_dice(2,6)) * roll_mod[self.color]
    
    def get_paydata_security(self):
        roll = dice.roll_one_die(6)
        if self.color == "Blue":
            if roll < 4: return "[No Defenses]"
            else: return "[Scramble IC " + str(self.get_ic_rating()) + "] "
        elif self.color == "Green":
            if roll < 3: return "[No Defenses]"
            elif roll < 5: return "[Scramble IC " + str(self.get_ic_rating()) + "] "
            else: return "[Data Bomb " + str(self.get_ic_rating()) + "] "
        elif self.color == "Orange":
            if roll < 2: return "[No Defenses]"
            elif roll < 4: return "[Scramble IC " + str(self.get_ic_rating()) + "] "
            elif roll < 6: return "[Data Bomb " + str(self.get_ic_rating()) + "] "
            else: return self.get_worm_security()
        else:
            if roll < 3: return "[Scramble IC " + str(self.get_ic_rating()) + "] "
            elif roll < 5: return "[Data Bomb " + str(self.get_ic_rating()) + "] "
            else: return self.get_worm_security()

    def get_worm_security(self):
        rating = dice.roll_one_die(6) + 3
        roll = dice.roll_multi_dice(2,6)
        if roll < 4: return "[Crashworm " + str(rating) + "] "
        elif roll < 6: return "[Deathworm " + str(rating) + "] "
        elif roll < 9: return "[Crashworm " + str(rating) + "] "
        elif roll < 11: return "[Tapeworm " + str(rating) + "] "
        else: return "[Ringworm " + str(rating) + "] "

    def get_ic_rating(self):
        roll = sum(dice.roll_multi_dice(2,6))
        if self.security_value < 5:
            if roll < 6: return 4
            elif roll < 9: return 5
            elif roll < 12: return 6
            else: return 8
        elif self.security_value < 8:
            if roll < 6: return 5
            elif roll < 9: return 7
            elif roll < 12: return 9
            else: return 10
        elif self.security_value < 11:
            if roll < 6: return 6
            elif roll < 9: return 8
            elif roll < 12: return 10
            else: return 12
        else:
            if roll < 6: return 8
            elif roll < 9: return 10
            elif roll < 12: return 11
            else: return 12

class security_sheaf(object):
    def __init__(self,color,SV):
        self.color = color
        self.SV = SV
        self.alert = "none"
        self.sheaf = self.get_sheaf()
    
    def get_next_trigger_step(self):
        if self.color == "Blue":
            return dice.roll_one_die(3) + 4
        elif self.color == "Green":
            return dice.roll_one_die(3) + 3
        elif self.color == "Orange":
            return dice.roll_one_die(3) + 2
        elif self.color == "Red":
            return dice.roll_one_die(3) + 1

    def get_alert(self):
        roll = srdice.roll_one_die(6)
        if self.alert == "none":
            if roll < 4: return self.get_reactive_white()
            elif roll < 6: return self.get_proactive_white()
            elif roll < 8: return self.get_reactive_grey()
            else:
                line = ""
                self.alert = "passive"
                if self.color == "Orange" or self.color == "Red":
                    line += self.get_reactive_grey() + ' / '
                return line + "Passive Alert"
        elif self.alert == "passive":
            if roll < 4: return self.get_proactive_white()
            elif roll < 6: return self.get_reactive_grey()
            elif roll < 8: return self.get_proactive_grey()
            else: 
                line = ""
                self.alert = "active"
                if self.color == "Orange" or self.color == "Red":
                    line += self.get_proactive_grey() + ' / '
                return line + "Active Alert"
        elif self.alert == "active":
            if roll < 4: return self.get_proactive_white()
            elif roll < 6: return self.get_proactive_grey()
            elif roll < 8: return self.get_black_ic()
            else: return "Shutdown"

    def get_ic_rating(self):
        roll = sum(dice.roll_multi_dice(2,6))
        if self.SV < 5:
            if roll < 6: return 4
            elif roll < 9: return 5
            elif roll < 12: return 6
            else: return 8
        elif self.SV < 8:
            if roll < 6: return 5
            elif roll < 9: return 7
            elif roll < 12: return 9
            else: return 10
        elif self.SV < 11:
            if roll < 6: return 6
            elif roll < 9: return 8
            elif roll < 12: return 10
            else: return 12
        else:
            if roll < 6: return 8
            elif roll < 9: return 10
            elif roll < 12: return 11
            else: return 12
        
    def get_reactive_white(self):
        roll = dice.roll_one_die(6)
        if roll < 3: return self.get_reactive_options() + "Probe" + " " + str(self.get_ic_rating())
        elif roll < 6: return self.get_reactive_options() + "Trace" + " " + str(self.get_ic_rating())
        else: return self.get_reactive_options() + "Tar Baby" + " " + str(self.get_ic_rating())

    def get_proactive_white(self):
        opt = self.get_proactive_options()
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 6: return opt + self.get_crippler_ripper() + " Crippler " + str(self.get_ic_rating())
        elif roll < 9: return opt + "Killer " + str(self.get_ic_rating())
        elif roll < 12: return opt + "Scout " + str(self.get_ic_rating())
        else: return "Construct"
    
    def get_reactive_grey(self):
        roll = dice.roll_one_die(6)
        if roll < 3: return self.get_reactive_options() + "Tar Pit " + str(self.get_ic_rating())
        elif roll < 4: return   self.get_trap_ic() + "Trace " + str(self.get_ic_rating())
        elif roll < 5: return   self.get_trap_ic() + "Probe " + str(self.get_ic_rating())
        elif roll < 6: return  self.get_trap_ic() + "Scout " + str(self.get_ic_rating())
        else: return "Construct"

    def get_proactive_grey(self):
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 6: return self.get_crippler_ripper() + " Ripper " + str(self.get_ic_rating())
        elif roll < 9: return self.get_proactive_options() + "Blaster " + str(self.get_ic_rating())
        elif roll < 12: return self.get_proactive_options() + "Sparky " + str(self.get_ic_rating())
        else: return "Construct"

    def get_black_ic(self):
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 5: return self.get_psychotropic_option() + "Psychotropic"
        elif roll < 8: return "Lethal Black"
        elif roll < 11: return "Non-Lethal Black"
        elif roll < 12: return "Cerebropathic"
        else: return "Construct"
          
    def get_crippler_ripper(self):
        roll = dice.roll_one_die(6)
        if roll < 3: return "Bod"
        elif roll < 4: return "Evasion"
        elif roll < 6: return "Masking"
        else: return "Sensor"

    def get_reactive_options(self):
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 5: return "Shield "
        elif roll < 6: return "Armor "
        elif roll < 8: return ""
        elif roll < 9: return self.get_trap_ic()
        elif roll < 10: return "Armor "
        else: return "Shift "

    def get_proactive_options(self):
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 4: return "Party Cluster "
        elif roll < 5: return "Expert Offense (" + str(dice.roll_one_die(3)) +") "
        elif roll < 6: return "Shifting "
        elif roll < 7: return "Cascading "
        elif roll < 8: return ""
        elif roll < 9: return "Armor "
        elif roll < 10: return "Shielding "
        elif roll < 11: return "Expert Defense (" + str(dice.roll_one_die(3)) +") "
        elif roll < 12: return self.get_trap_ic()
        else: return self.get_proactive_options() + "/ " + self.get_proactive_options()

    def get_trap_ic(self):
        roll = sum(dice.roll_multi_dice(2, 6))
        if roll < 3: return "[Data Bomb " + str(self.get_ic_rating()) + "] "
        elif roll < 6: return "[Blaster " + str(self.get_ic_rating()) + "] "
        elif roll < 9: return "[Killer " + str(self.get_ic_rating()) + "] "
        elif roll < 12: return "[Sparky " + str(self.get_ic_rating()) + "] "
        else: return '[' + self.get_black_ic() + " " + str(self.get_ic_rating()) + "] "

    def get_psychotropic_option(self):
        roll = dice.roll_one_die(6)
        if roll < 3: return "Cyberphobia "
        elif roll < 4: return "Frenzy "
        elif roll < 5: return "Judas "
        else: return "Positive Conditioning "
    
    def get_sheaf(self):
        sheaf = []
        trigger_step = 0
        line = ""
        while "Shutdown" not in line:
            line = ""
            trigger_step += self.get_next_trigger_step()
            line = str(trigger_step)+(" " * (3 - len(str(trigger_step)))) + " - " + self.get_alert()
            sheaf.append(line)
        return sheaf

class program(object):
    def __init__ (self,name, modifier, rating):
        self.modifier = modifier
        self.rating = rating
        self.size = (self.rating ** 2) * self.modifier

#a = host()
#for line in a.sheaf:
#    print line
