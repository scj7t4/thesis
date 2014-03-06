
set terminal epslatex  
set output 'TRANS-RT-SUC-64-COMPARE.tex'
set boxwidth 3 absolute
set title "Simulated versus Experimental Time In Group: Two Node (SUC 64ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Seconds)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 600.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
set key right bottom
plot 'TRANS-RT-SUC-64.dat'        using 1:3 ti "Experimental Value", \
     'TRANS-RT-SUC-64.dat'  using 1:2 ti "Markov Value"
