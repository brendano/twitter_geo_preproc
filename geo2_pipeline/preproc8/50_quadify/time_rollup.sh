#!/bin/bash
function quints_to_just_time() {
  mawk '
  {times[$1]=1; words[$4]=1; counts[$1","$4] += 1} 
  END{
  for (w in words) {
  for (t in times) { 
    c = counts[t "," w]
    if (c)
      print t,w,c
  } } }
  '
}

set -eu
target=$1
[ -d $target ]
mkdir -p $target/t.w.uc
for f in $target/quints/wb=*; do
  echo $f
  cat $f | quints_to_just_time > $target/t.w.uc/$(basename $f)
done
    

