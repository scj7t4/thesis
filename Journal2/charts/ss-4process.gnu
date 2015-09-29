reset
procs = 4
filename = 'ss-'.procs.'process'
plottitle = ''.procs.' Process'

set terminal epslatex size SIZE_X,SIZE_Y color colortext
set output filename.'.tex'
set boxwidth 3 absolute
set key invert top left at -4.3,1.05
set title 'Steady State For '.plottitle.' Model'
#set xrange [ -.0500000 : 1.050000 ] noreverse nowriteback
set auto x
set xtics nomirror rotate by -45 scale 0
set ylabel "Probability of State\nAverage Group Size (AGS) as a Fraction"
set xlabel "Probability of Delivery"
set yrange [ 0.00000 : 1.10 ] noreverse nowriteback
set style data histogram
set style histogram rowstacked
set style fill pattern border
set boxwidth 0.75
everyother(col) = (int(column(col)*100-5) % 10 == 0) ? stringcolumn(1) : ""
plot 'data/'.filename.'.dat' using 3:xticlabels(everyother(1)) lc rgbcolor "black" title 'Group Size 2',\
     for [i=4:(procs+1)] '' using i lc rgbcolor "black" title 'Group Size '.(i-1),\
     'data/ss-means.dat' using ($4/100.0) with linespoints title 'AGS as a Fraction' lc rgbcolor "black"
