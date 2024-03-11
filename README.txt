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

for f in portfolio*.csv; do starting_date=$(echo $f | cut -d '_' -f 3 | cut -d '.' -f 1); final_total=$(cat $f | tail -1 | rev | cut -d ',' -f 1 | rev); echo "${starting_date}: ${final_total}"; done

   (also present for your convenience as get-all-end-results.sh)
