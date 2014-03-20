
set terminal epslatex  
set output '2NODE-SUC-200-COMPARE.tex'
set boxwidth 3 absolute
set title "Simulated versus Experimental Time In Group: Two Node (SUC 200ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Minutes)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 5
set style line 2 lt 1 lc rgb "black" lw 5
set key right bottom
plot '2NODE-SUC-100.dat' using 1:9:9:9:9 with candlesticks ls 2 notitle,      ''                 using 1:8:7:11:10 with candlesticks ls 1 ti "Experimental Value", \
     '2NODE-SUC-200-SIMUL.dat'  using 1:3 ti "SharpE Uptime" ps 2 linewidth 2
