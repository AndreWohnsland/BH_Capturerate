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
# the bonus Capturerate (range) you want to cover (in percent) default is 50 - 450, step 50
bonusmin_CR = 50
bonusmax_CR = 450
bonusstep_CR = 50
bonus_CR = list(range(bonusmin_CR, bonusmax_CR+bonusstep_CR, bonusstep_CR))
# how many times you want to simulate till you get all familars (the more, the more accurate)
number_of_sim = 100
# if you want to bribe or not bribe
do_bribe = True

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

CR_treshhold = [base_CR_treshhold * ((x)/100 + 1) for x in bonus_CR]
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
print(template.format("minimal bonus CR", bonusmin_CR))
print(template.format("maximal bonus CR", bonusmax_CR))
print(template.format("step bonus CR", bonusstep_CR))
print(template.format("capturerate", capturerate))
print(template.format("Persuaderate", base_PC_treshhold))
print(template.format("amount Monster/Dungeon", amount_m))
print(template.format("diversity Monster", diversity))

diagram_title = ("Trys and Costs to get %i %s Fams in %s%s (%1.2f multiplier)"
                 " | different capturerate bonus") % (
                     fam_amount, monstertype,
                     raidtier, difficulty,
                     CR_multiplier/100)

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

from copy import deepcopy
fig, ax = plt.subplots(len(bonus_CR), 3, figsize =(15, len(bonus_CR)* 5))
diagram_title = ("Bribing: %i %s Fams in %s%s (%1.2f multiplier)"
                 " | different capturerate bonus") % (
                     fam_amount, monstertype,
                     raidtier, difficulty,
                     CR_multiplier/100)
# fig.suptitle(diagram_title, fontsize=22, y = 0.90)
plt.tight_layout(h_pad = 4, w_pad = 3)
for row in range(0, len(bonus_CR)):
    wX = []
    vY = []
    uGC = []
    y = 1
    while y <= number_of_simulations:
        famcount = 0
        gem_cost = 0
        z = 0
        while famcount < fam_amount:
            cr_simulation(CR_treshhold[row], max_CR, base_PC_treshhold, max_PC, maxtries, do_bribe)
            z += 1
            gem_cost += r_cost*m_cor_f
        wX.append(round(y*m_cor_f))
        vY.append(round(z*m_cor_f))
        uGC.append(round(gem_cost))
        y += 1
        
    vY_uo = deepcopy(vY)
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
    if do_bribe:
        storevar = fam_amount*b_cost
    
    print("~~~~~~~~~~~~~~~ CR Bonus: {} ~~~~~~~~~~~~~~~".format(bonus_CR[row]))
    print("min | max | average trys:    ",
          min(vY), "|", max(vY), "|",
          round(sum_try/len(vY)))
    print("Average Cost | Raidcosts:    ",
          round(sum_gc/len(uGC)), "|",
          (round(sum_gc/len(uGC) - storevar)))
    
    colcolor = ['c', 'r', 'g']
    Y_array = [vY_uo, vY, uGC]
    sum_array = [sum_try, sum_try, sum_gc] 
    header_array = [
        'CR Bonus: {}, Runs (unsorted)'.format(bonus_CR[row]),
        'Runs (sorted)',
        'Cost'
    ]
    Ylabel_array = [
        'Number of Raids to get {} Fams'.format(fam_amount),
        'Number of Raids to get {} Fams'.format(fam_amount),
        'Amount of Gems to get {} Fams'.format(fam_amount)
    ]
    text_array = [
        "average = %i | min = %i | max = %i" % ((sum_try/len(vY)), min(vY), max(vY)),
        "average = %i | min = %i | max = %i" % ((sum_try/len(vY)), min(vY), max(vY)),
        "average = %i | min = %i | max = %i" % ((sum_gc/len(uGC)), min(uGC), max(uGC))
    ]
    
    for col in range(0, 3):
        ax_now = ax[row, col]
        ax_now.plot(Y_array[col], color=colcolor[col])
#         ax_now.set_ylabel(Ylabel_array[col], fontsize=14)
#         ax_now.set_xlabel('Simulation Number', fontsize=14)
        ax_now.set_title(header_array[col], fontsize=18)
        ax_now.text(number_of_sim/10, sum_array[col]/len(Y_array[col]), 'average', fontsize=12, va='center', ha='center', backgroundcolor='w')
        ax_now.axhline(sum_array[col]/len(Y_array[col]), color='k', linestyle='-.')
        ax_now.text(0.05, 0.95, text_array[col], verticalalignment='top', horizontalalignment='left', transform=ax_now.transAxes, fontsize=12, backgroundcolor='w')
        ax_now.grid(True, linestyle='--')
        ax_now.tick_params(labelsize=14)
        ax_now.set_xlim([0, number_of_sim])
        
plt.savefig("range_t{}_{}{}_{}.png".format(number_of_sim, raidtier, difficulty, monstertype), dpi=300)


plt.show()