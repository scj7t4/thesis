
set terminal epslatex  
set output '2NODE-SRC-200-SIZE.tex'
set boxwidth 3 absolute
set title "Average Group Size: Two Node (SRC - 200ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set yrange [ 0 : 4.49 ]
set ylabel "Size of Average Group"
set xlabel "Network Reliability"
#set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 5
set style line 2 lt 1 lc rgb "black" lw 5
plot '2NODE-SRC-200.dat' using 1:14:14:14:14 with candlesticks ls 2 notitle,      ''                  using 1:13:12:16:15 with candlesticks ls 1 notitle
