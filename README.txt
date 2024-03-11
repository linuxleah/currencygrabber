USAGE:

1) create a basket of currencies (Gold is also supported);
   e.g., here might be "basket1.txt":

CAD: 100k
CHF: 200k
EUR: 150k
JPY: 150k
AUD: 50k
NZD: 50k
Gold: 100k
GBP: 100k
SEK: 50k
NOK: 50k

2) Ensure you have up to date historical data:
   python3 currency-grabber.py

3) Run the simulations for your basket:
   python3 basket-simulator.py

4) Analyse the final totals of each run:
   python3 analyse-results.py

   You can also get just the final totals of each run,
   though this is less telling of actual daily performance:
   sh get-all-end-results.sh

OPTIONAL: A simpler way of running a complete end to end analysis
          (i.e. running steps 3 and 4 from above together)
          is provided in the form of 'analyse.sh':

          bash analyse.sh basket1.txt

