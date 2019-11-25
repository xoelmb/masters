# 3.a
cat mbio.sample.sam | grep -vE "^@" | head -n 500 | tail -n 1
# 3.b
awk '{print $10}' mbio.sample.sam | fold -w 1 | sort | uniq -c | grep -E "[a-z]" | sort -rn | head -n 1
# 3.c
awk 'NR%4==1{a='