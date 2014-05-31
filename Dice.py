from random import choice

class dice (object):
        
    def roll_one_die(self,sides):
        return int(choice(range(1,sides+1)))
    
    def roll_multi_dice(self,dice,sides):
        results = []
        for _ in range (dice):
            results.append(choice(range(1,sides+1)))
        return results

class shadowrun_dice(dice):
    def roll_one_die(self,sides = 6):
        total = 0
        result = int(choice(range(1,sides+1)))
        while result == 6:
            total += result
            result = int(choice(range(1,sides+1)))
        return total + result

    def roll_multi_dice(self,dice):
        results = []
        for _ in range (dice):
            results.append(self.roll_one_die(6))
        return results
    
    def success_test(self,pool,TN):
        results = self.roll_multi_dice(pool, 6)
        successes = 0
        for result in results:
            if result >= TN and result >= 2: successes += 1
        return successes
    
    def get_successes (self):
        pool = int(raw_input("How many dice are in the dice pool? - "))
        TN = int(raw_input("What is the target number of this action? - "))
        return self.success_test(pool, TN)


if __name__ == "__main__":
    number = raw_input("How Many Dice? > ")
    a = shadowrun_dice()
    print a.roll_multi_dice(int(number))
    