reset
n=20 #number of intervals
max=100. #max value
min=0. #min value
width=(max-min)/n #interval width
#function used to map a value to the intervals
hist(x,width)=width*floor((x)/width)
set terminal epslatex size SIZE_X,SIZE_Y color colortext  
set output '2NODE-SUC-100-LDR-FEVENTS.tex'
set boxwidth 0.9*width
set title "Two Process, Number Of Detected Leader Failures (SUC - 100ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set yrange [ 0 : ]
set ylabel "Number of Collected Events"
set xlabel "Probability of Delivery"
set style fill solid 0.5
#set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "black" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot '2NODE-SUC-100-LDR-FAIL.dat' using (hist($1,width)):2 smooth freq with boxes lc 2 notitle
#plot "data.dat" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
#plot '2NODE-SUC-100.dat' using 1:14:14:14:14 with candlesticks ls 2 notitle,      ''                  using 1:13:12:16:15 with candlesticks ls 1 notitle
