#!/bin/bash

dir=/deac/thonhauserGrp/chakrad/calculations/atomandmolecule-qe6.2.1-i2012-C6modif/test_solid_new_2/AlP/

for folder in $dir/DF3*/;do
echo $folder
cd $folder/
rm -rf *.txt
for pos in *;do
echo $pos
cd $pos/
energy=`cat output* | grep -i '!' | tail -1 | awk '{printf "%4.10f", $5*13.605698065894}'`
a_lat=`echo $pos | awk '{print $1}'`
echo $a_lat $energy  >>  ../tmp.txt
cd ../
done
echo "2     # Unit of energy for input values
1  # Volume of unit cell/cell used
8. 11. 70 # minimal/maximal value for lattice const.(in bohr), number of points to calculate
21   # number of energy pairs (lattice const(in bohr) & energy(in eV))" > header.txt
sort -n tmp.txt > energy_vs_lattice.txt
cat header.txt energy_vs_lattice.txt > Elatt.murn.in
../.././birch-murn < Elatt.murn.in > Elatt.birch-murn.out 
cd ../
done
