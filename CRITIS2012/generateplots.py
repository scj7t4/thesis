from string import Template
import subprocess

GROUPTIME="""
set terminal pngcairo  transparent enhanced font "sans-serif,12" fontscale 1.0 size 800, 600 
set output '${dataset}-GROUP.png'
set boxwidth 3 absolute
set title "Time In Group: $type ($protocol ${resend}ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set ylabel "In Group Time (Minutes)"
set xlabel "Network Reliability"
set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot '${dataset}.dat' using 1:9:9:9:9 with candlesticks ls 2 notitle,      ''                 using 1:8:7:11:10 with candlesticks ls 1 notitle
"""

GROUPSIZE="""
set terminal pngcairo  transparent enhanced font "sans-serif,12" fontscale 1.0 size 800, 600 
set output '${dataset}-SIZE.png'
set boxwidth 3 absolute
set title "Average Group Size: $type ($protocol - ${resend}ms Resend)" 
set xrange [ -5.00000 : 105.0000 ] noreverse nowriteback
set yrange [ 0 : 4.49 ]
set ylabel "Size of Average Group"
set xlabel "Network Reliability"
#set yrange [ 0.00000 : 10.0000 ] noreverse nowriteback
set style line 1 lt 1 lc rgb "red" lw 1
set style line 2 lt 1 lc rgb "black" lw 1
plot '${dataset}.dat' using 1:14:14:14:14 with candlesticks ls 2 notitle,      ''                  using 1:13:12:16:15 with candlesticks ls 1 notitle
"""

DATASETS= [ {'dataset':'TRANS-SRC-100','resend':100,'protocol':'SRC','type':'Transient Partition'},
            {'dataset':'TRANS-SRC-200','resend':200,'protocol':'SRC','type':'Transient Partition'},
            {'dataset':'TRANS-SUC-100','resend':100,'protocol':'SUC','type':'Transient Partition'},
            {'dataset':'TRANS-SUC-200','resend':200,'protocol':'SUC','type':'Transient Partition'},
            {'dataset':'2NODE-SRC-100','resend':100,'protocol':'SRC','type':'Two Node'},
            {'dataset':'2NODE-SRC-200','resend':200,'protocol':'SRC','type':'Two Node'},
            {'dataset':'2NODE-SUC-100','resend':100,'protocol':'SUC','type':'Two Node'},
            {'dataset':'2NODE-SUC-200','resend':200,'protocol':'SUC','type':'Two Node'} ]

for x in DATASETS:
    filename = x['dataset']+"-GROUP.gnu"
    f = open(filename,"w")
    contents = Template(GROUPTIME)
    f.write(contents.substitute(x))
    f.close()
    subprocess.call(["gnuplot",filename])
    filename = x['dataset']+"-SIZE.gnu"
    f = open(filename,"w")
    contents = Template(GROUPSIZE)
    f.write(contents.substitute(x))
    f.close()
    subprocess.call(["gnuplot",filename])
