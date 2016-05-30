
set terminal epslatex size SIZE_X,SIZE_Y color colortext  
set output '2NODE-SRC-100-SIZE.tex'
set boxwidth 3 absolute
set title "Average Group Size:\n Two Process (SRC - 100ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set yrange [ 0 : 4.49 ]
set ylabel "Size of Average Group"
set xlabel "Probability of Delivery"
#set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot '2NODE-SRC-100.dat' using 1:14:14:14:14 with candlesticks ls 2 notitle,      ''                  using 1:13:12:16:15 with candlesticks ls 1 notitle
