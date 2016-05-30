
set terminal epslatex size SIZE_X,SIZE_Y color colortext  
set output 'TRANS-RT-SUC-64-COMPARE.tex'
set boxwidth 3 absolute
set title "Simulated versus Experimental Time In Group:\n Transient Partition (SUC 64ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Seconds)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 600.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
set style line 3 lt 1 lc rgb "black" lw 1 pointtype 2
set key right bottom
plot 'TRANS-RT-SUC-64.dat' using 1:6:6:6:6 with candlesticks ls 2 notitle,      ''                 using 1:5:4:8:7 with candlesticks ls 1 ti "Experimental Value", \
     'TRANS-RT-SUC-64.dat'  using 1:2 ti "Markov Value" ls 3
