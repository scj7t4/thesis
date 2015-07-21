reset
filename = 'ss-means'
plottitle = 'Mean Group Size As Pct During Omission Failure'

set terminal epslatex size SIZE_X,SIZE_Y color colortext
set output filename.'.tex'
set boxwidth 3 absolute
set key invert reverse top left inside
set title plottitle
#set xrange [ -.0500000 : 1.050000 ] noreverse nowriteback
set auto x
set xtics nomirror rotate by -45 scale 0
set ylabel "Average Group Size As A Percentage of All Processes"
set xlabel "Probability of Delivery"
set yrange [ 0.00000 : 1.10 ] noreverse nowriteback
set style data linespoints
set key autotitle columnhead
do for [i=1:10] {
	set style line i lc rgbcolor "black"
}
plot 'data/'.filename.'.dat' using 1:2 ls 1 title "200 Processes",\
     '' using 1:3 ls 2 title "100 Processes",\
	 '' using 1:4 ls 3 title "50 Processes",\
	 '' using 1:5 ls 4 title "25 Processes",\
	 '' using 1:6 ls 5 title "10 Processes",\