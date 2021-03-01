# Progetto-Ethereum-Web3-di-Giacomo-Colella

ENVIRONMENT TOKENS.
-------------------
A platform that allows you to accumulate tokens by producing energy through solar panels and or wind turbines.


WATCH THIS
----------------------------------
To initialize the system follow the following steps:

1)Pip install requirements.txt

2)Launch Ganache program. 

3)Move into blockc/build directory and type:
    truffle compile (command).
    truffle migrate --network development
    
4)Move into main/utils.py and change the value of 'addr' in getInfoToken() function with the contract address taken from ganache.

5)Now create the superuser with which to access to control panel.

6)Finally run "python or python3 manage.py runserver" command.





How does it work?
-----------------

Every 4 Watt you produce you get a reward of 1 GreenToken. On average, a single solar panel produces about 0.5 watts per day.
Considering the hours of sunshine that are around 13 hours, about 0.04 watts of power are produced in one hour.
Let's take a 3kw photovoltaic system that can produce about 3400-4000w of power in a year, 
or the energy needs of an average family, we get a profit of about 850-1000 GreenToken.
