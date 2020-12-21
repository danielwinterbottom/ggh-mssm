run=${1}

rm -r gridpack

mkdir -p gridpack
cp *.dat gridpack/.
cp powheg.input-base gridpack/.
cp pwgseeds.dat gridpack/.
cp pwhg_main gridpack/.
cp runcmsgrid.sh gridpack/.
cp pwg-rwl.dat gridpack/.
cp mod_scalup.py gridpack/.
cp -r lib gridpack/.

cd gridpack

rm pwgcounters*
rm pwg-st3-00[0-9][1-9]-stat.dat	# keep some info
rm pwg-????-stat.dat

tar -czvf ggh_powheg_${run}.tar.gz *

cd ..
