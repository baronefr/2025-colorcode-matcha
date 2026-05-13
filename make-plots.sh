
script="plt_thres.py"

for case in "ampd-1c" "ampd-dc" "srx-1c" "srx-dc"; do
    echo "Processing case: $case"
    python3 $script $case
done

python3 plt_twirl.py
