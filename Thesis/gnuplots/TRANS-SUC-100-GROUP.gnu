
set terminal epslatex  
set output 'TRANS-SUC-100-GROUP.tex'
set boxwidth 3 absolute
set title "Time In Group: Transient Partition (SUC 100ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Minutes)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot 'TRANS-SUC-100.dat' using 1:9:9:9:9 with candlesticks ls 2 notitle,      ''                 using 1:8:7:11:10 with candlesticks ls 1 notitle
