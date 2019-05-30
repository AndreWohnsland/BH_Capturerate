import matplotlib
import random
import matplotlib.pyplot as plt
import time
from matplotlib.ticker import FuncFormatter


"""
10 x 3 = 30 Tries
3 different Monsters -> 10 Subtries per Dungeon (Except R1)
1,5% * 7% = 0,105% Base CR -> 105 of 100000 for RND
15% Succes at CR -> 15 of 100 for RND
You can easily estimate the average needed amount of dungeons (D)
for an wished amount of Familars (A) with the amount of Monsters (Ma)
and their Capturerate (CR) as well persute Rate (PR):
D = A/(Ma*CR*PR) | If bribe: PR = 1
For the distribution the MC-Simulation is used
"""
global famcount
global gem_cost
famcount = 0
gem_cost = 0

# R1    = 10 (epic) / 15 (boss) (2x10 monster)
# R2    = 7 (epic) / 12 (boss) (3x10 monster)
# R3+   = 5 (epic) / 12 (boss) (3x10 monster)
# R1/R2/R3 or R3+(default), Epic or Boss(default), N / H / Hc(default)

# Change the Values HERE !
# R1, R2 or r3 (everything above is similar)
raidtier = "R3"
# Epic oder Boss
monstertype = "Epic"
# N, H or Hc
difficulty = "Hc"
# how many familars you want to get
fam_amount = 5
# the price in Gems for a Raidbasked (20 Raidshards)
basket_cost = 600
# the bonus Capturerate in your Profile (in percent)
bonus_CR = 340
# how many times you want to simulate till you get all familars (the more, the more accurate)
number_of_sim = 100

# you may set this to true, then the upper and lower 2% of the results got removed
cutends = False
if cutends:
    number_of_simulations = number_of_sim / 0.96
    testingnumber = int(number_of_simulations/50)
else:
    number_of_simulations = number_of_sim
    
if (monstertype == "Epic") or (monstertype == "epic"):
    capturerate = 1.5
    base_PC_treshhold = 15
    b_cost = 800
    diversity = 3
    if raidtier == "R1":
        CR_multiplier = 10
        amount_m = 20
    elif raidtier == "R2":
        CR_multiplier = 7
        amount_m = 30
    else:
        CR_multiplier = 5
        amount_m = 30
else:
    capturerate = 1
    base_PC_treshhold = 10
    amount_m = 1
    b_cost = 1600
    diversity = 1
    if raidtier == "R1":
        CR_multiplier = 15
    else:
        CR_multiplier = 12

if difficulty == "N":
    difficulty_mult = 1
elif difficulty == "H":
    difficulty_mult = 1.5
else:
    difficulty_mult = 2

m_cor_f = 1
if (raidtier == "R1") and ((monstertype == "Epic") or (monstertype == "epic")):
    # since it uses only even numbers in R1
    # are 6.66 monsters average, but 7 is used
    m_cor_f = 1.05

base_CR_treshhold = capturerate * difficulty_mult * CR_multiplier * 10
max_CR = 100000
max_PC = 100
r_cost = basket_cost/20

CR_treshhold = base_CR_treshhold * ((bonus_CR)/100 + 1)
maxtries = round(amount_m/diversity)

template = "{:30} | {:^20} "
print("#################################################")
print("################# used Data #####################")
print("#################################################")
print(template.format("Amount of Simulations", number_of_sim))
print(template.format("Raidtier", raidtier))
print(template.format("Difficulty", difficulty))
print(template.format("Monstertype", monstertype))
print(template.format("Amount of Familars", fam_amount))
print(template.format("bonus CR", bonus_CR))
print(template.format("capturerate", capturerate))
print(template.format("Persuaderate", base_PC_treshhold))
print(template.format("amount Monster/Dungeon", amount_m))
print(template.format("diversity Monster", diversity))

diagram_title = ("Trys and Costs to get %i %s Fams in %s%s (%1.2f multiplier)"
                 " | %i capturerate bonus") % (
                     fam_amount, monstertype,
                     raidtier, difficulty,
                     CR_multiplier/100, bonus_CR)

print("\n~~~~~~~~~~~~~~~ Starting Simulation ~~~~~~~~~~~~~~~\n")

def cr_simulation(CR, mCR, PC, mPC, mT, bribe):
    global famcount
    x = 0
    while x < mT:
        if rollcheck(CR, mCR):
            if rollcheck2(PC, mPC, bribe):
                famcount += 1
        x += 1


def rollcheck(CR, mCR):
    rolled_number = random.randint(1, mCR)
    if rolled_number <= CR:
        # print("CR succeeded",rolled_number)
        return True
    else:
        # print("CR failed",rolled_number)
        return False


def rollcheck2(PC, mPC, bribe):
    global gem_cost
    if bribe:
        gem_cost += b_cost
        return True
    else:
        rolled_number = random.randint(1, mPC)
        if rolled_number <= PC:
            # print("P succeeded",rolled_number)
            return True
        else:
            # print("P failed",rolled_number)
            return False

do_bribe = [True, False]
fig, ax = plt.subplots(2, 2, figsize =(15, 15))
fig.suptitle(diagram_title, fontsize=22)
for cols in range(0, 2):
    wX = []
    vY = []
    uGC = []
    y = 1
    while y <= number_of_simulations:
        famcount = 0
        gem_cost = 0
        z = 0
        while famcount < fam_amount:
            cr_simulation(CR_treshhold, max_CR, base_PC_treshhold, max_PC, maxtries, do_bribe[cols])
            z += 1
            gem_cost += r_cost*m_cor_f
        wX.append(round(y*m_cor_f))
        vY.append(round(z*m_cor_f))
        uGC.append(round(gem_cost))
        y += 1
        
    vY.sort()
    uGC.sort()
    if cutends:
        del vY[:testingnumber]
        del vY[-testingnumber:]
        del uGC[:testingnumber]
        del uGC[-testingnumber:]
        
    sum_try = 0
    sum_gc = 0
    for line1, line2 in zip(vY, uGC):
        sum_try += line1
        sum_gc += line2
    storevar = 0
    if do_bribe[cols]:
        storevar = fam_amount*b_cost
    
    print("~~~~~~~~~~~~~~~ Bribe: {} ~~~~~~~~~~~~~~~".format(do_bribe[cols]))
    print("min | max | average trys:    ",
          min(vY), "|", max(vY), "|",
          round(sum_try/len(vY)))
    print("Average Cost | Raidcosts:    ",
          round(sum_gc/len(uGC)), "|",
          (round(sum_gc/len(uGC) - storevar)))
    
    colcolor = ['c', 'r']
    Y_array = [vY, uGC]
    sum_array = [sum_try, sum_gc] 
    header_array = [
        'Runs for {} Fams (Bribe = {})'.format(fam_amount, do_bribe[cols]),
        'Cost for {} Fams (Bribe = {})'.format(fam_amount, do_bribe[cols])
    ]
    Ylabel_array = [
        'Rumber of Raids to get {} Fams'.format(fam_amount),
        'Amount of Gems to get {} Fams'.format(fam_amount)
    ]
    text_array = [
        "average = %i | min = %i | max = %i" % ((sum_try/len(vY)), min(vY), max(vY)),
        "average = %i | min = %i | max = %i" % ((sum_gc/len(uGC)), min(uGC), max(uGC))
    ]
    
    for row in range(0, 2):
        ax_now = ax[row, cols]
        ax_now.plot(Y_array[row], color=colcolor[cols])
        ax_now.set_ylabel(Ylabel_array[row], fontsize=14)
        ax_now.set_xlabel('Simulation Number', fontsize=14)
        ax_now.set_title(header_array[row], fontsize=18)
        ax_now.text(number_of_sim/10, sum_array[row]/len(Y_array[row]), 'average', fontsize=12, va='center', ha='center', backgroundcolor='w')
        ax_now.axhline(sum_array[row]/len(Y_array[row]), color='k', linestyle='-.')
        ax_now.text(0.05, 0.95, text_array[row], verticalalignment='top', horizontalalignment='left', transform=ax_now.transAxes, fontsize=12, backgroundcolor='w')
        ax_now.grid(True, linestyle='--')
        ax_now.tick_params(labelsize=14)
        ax_now.set_xlim([0, number_of_sim])
        
    fig.savefig('specific_t{}_CR{}_{}{}_{}.png'.format(number_of_sim, bonus_CR, raidtier, difficulty, monstertype), dpi=600)


plt.show()