for f in portfolio*.csv; do starting_date=$(echo $f | cut -d '_' -f 3 | cut -d '.' -f 1); final_total=$(cat $f | tail -1 | rev | cut -d ',' -f 1 | rev); echo "${starting_date}: ${final_total}"; done
