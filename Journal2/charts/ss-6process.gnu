reset
procs = 6
filename = 'ss-'.procs.'process'
plottitle = ''.procs.' Process'

set terminal epslatex size SIZE_X,SIZE_Y color colortext
set output filename.'.tex'
set boxwidth 3 absolute
set key invert reverse top left inside
set title 'Steady State For '.plottitle.' Model'
#set xrange [ -.0500000 : 1.050000 ] noreverse nowriteback
set auto x
set xtics nomirror rotate by -45 scale 0
set ylabel "Probability of State"
set xlabel "Probability of Delivery"
set yrange [ 0.00000 : 1.10 ] noreverse nowriteback
set style data histogram
set style histogram rowstacked
set style fill pattern border
set boxwidth 0.75
plot 'data/'.filename.'.dat' using 3:xticlabels(1) lc rgbcolor "black" title 'Group Size 2',\
     for [i=4:(procs+1)] '' using i lc rgbcolor "black" title 'Group Size  '.(i-1)
