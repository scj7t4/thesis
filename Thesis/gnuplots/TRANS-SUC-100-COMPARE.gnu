
set terminal epslatex size SIZE_X,SIZE_Y color colortext  
set output 'TRANS-SUC-100-COMPARE.tex'
set boxwidth 3 absolute
set title "Comparision Between Experimental and SharpE (Transient Partition, 100ms Resend, SUC)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Minutes)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
set style line 3 lt 1 lc rgb "black" lw 1 pointtype 2
plot 'TRANS-SUC-100.dat' using 1:9:9:9:9 with candlesticks ls 2 notitle,      ''                 using 1:8:7:11:10 with candlesticks ls 1 ti "Experimental Value", \
     'TRANS-SUC-100-SIMUL.dat'  using 1:4 ti "SharpE Uptime" ls 3
