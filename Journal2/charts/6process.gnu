reset
filename = '6process'
plottitle = '6 Process' 
criticalvalue = 43.8

f(x) = criticalvalue

set terminal epslatex size SIZE_X,SIZE_Y color colortext 
set output filename.'.tex'
set boxwidth 3 absolute
set title 'Error For '.plottitle.' model'
set xrange [ -.0500000 : 1.050000 ] noreverse nowriteback
set ylabel "Error ($\\chi^2$)"
set xlabel "Probability of Delivery"
set yrange [ 0.00000 : (criticalvalue*1.25) ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot filename.'.dat' using 1:2 with points ls 2 title 'Measured Error', \
	 f(x) title 'Critical Value' with lines ls 1 dashtype 2