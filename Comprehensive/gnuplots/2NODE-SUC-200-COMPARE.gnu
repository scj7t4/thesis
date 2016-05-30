
set terminal epslatex size SIZE_X,SIZE_Y color colortext  
set output '2NODE-SUC-200-COMPARE.tex'
set boxwidth 3 absolute
set title "Simulated versus Experimental In-Group Time:\n Two Process (SUC 200ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Minutes)"
set xlabel "Probability of Delivery"
set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
set style line 3 lt 1 lc rgb "black" lw 1 pointtype 2
set key right bottom
set key box ls 1
set key width -5.25
set key opaque
plot '2NODE-SUC-100.dat' using 1:9:9:9:9 with candlesticks ls 2 notitle,      ''                 using 1:8:7:11:10 with candlesticks ls 1 ti "Experimental Value", \
     '2NODE-SUC-200-SIMUL.dat'  using 1:3 ti "SharpE Uptime" ls 3
