# Bit Heroes Capture Rate Simulator

Hello everyone! This is a little tool which uses the RNG logic behind the persuade and capture rate of familiars in the Bit Heroes Game. 
On top of that, it uses a Monte Carlo Simulation to not only get the average, but also the minimal and maximal amount of tries needed to get a certain amount of a familiar as well as the distribution. 
It also calculates the gem costs (based on bribing and not bribing, as well Raid Shard cost). Currently only Raid familiars are supported, this may change in the future.

## Minimal Requirements

```
- Python 3.5
- matplotlib
```

## Install Matplotlib

To install matplotlib just use the pip command on your console:
```
pip install matplotlib
```

## Changing Simulation Values

There are two different sort of simulations you can do. 
The standard version `Captruerate_MC` simulates at a given bonus Capturerate and calculates for bribing and not bribing. 
The extended version `Captruerate_MC_diffCR` takes a min, max and step Capturerate as well if you want to bribe or not and calculates the rates. 
Other Variables like raidtier, monster rarity, difficulty, raid basket cost, number of simulation and other things can be chosen as well and are explained in each comment below.


## Some Example Pictures

A single Simulation:\

![alt text](https://github.com/AndreWohnsland/BH_Capturerate/blob/master/specific_t100000_CR340_R3Hc_Epic.png "Single Simulation for bribe and not bribe")

a Range:\

![alt text](https://github.com/AndreWohnsland/BH_Capturerate/blob/master/range_t100_R3Hc_Epic.png "Simulation of different Capturerates")

