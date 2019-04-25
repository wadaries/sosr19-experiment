set termoption dash
set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 back linestyle 80
set terminal pdfcairo size 4,3
set output 'Gnuplot\pdf\brute-force.pdf'
set multiplot layout 2,2

set xtics nomirror font ",8" offset 0,0.5
set ytics nomirror font ",8" offset 0.5,0

#set title 'a' font ",8" 
#set ylabel "delay(ms)" font ",8" offset 4,0 
#set xlabel "subsumed clause size" font ",8" offset 0,1.5
#set key top left font ",5"
#set style data histogram
#set style histogram cluster gap 1
#set style fill solid border rgb "black"
#set boxwidth 0.5
#set auto x
#set yrange [0:*]
#plot 'F:\git\Wiser\output\brute-force.txt' using 9:xtic(13) notitle,\
#     '' using 0:($9+30):(sprintf("%.2f", $9)) with labels font ",5" notitle

set title 'a' font ",8" 
set ylabel "delay(ms)" font ",8" offset 4,0 
set xlabel "N (size of P2)" font ",8" offset 0,1.5
set key top left font ",5"
#set style data histogram
#set style histogram cluster gap 1
set style fill solid border rgb "black"
set boxwidth 1
set xrange [0:*]
set xtics 2,2,16
#set yrange [0:*]
#set bars 2
plot 'F:\git\Wiser\output\brute-force.txt' using 8:9 with boxes title 'M=4',\
     '' using 8:($9+30):(sprintf("%.2f", $9)) with labels font ",5" notitle

set title 'b' font ",8" 
set boxwidth 0.06
set logscale x
set xrange [1.5:*]
set xtics 2,2,16
set logscale y
plot 'F:\git\Wiser\output\brute-force.txt' using 8:9 with boxes  title 'M=4',\
     '' using 8:($9*2):(sprintf("%.2f", $9)) with labels font ",5" notitle

set title 'c' font ",8" 
unset logscale x
set xrange [0:*]
set xtics 2,2,16
unset logscale y
set ytics 1000
plot 'F:\git\Wiser\output\brute-force.txt' using 2:3 with linespoints pt 6 ps 0.5 title 'M=2',\
     '' using 5:6 with linespoints pt 8 ps 0.5 title 'M=4',\
     '' using 8:9 with linespoints pt 10 ps 0.5 title 'M=8',\
     '' using 11:12 with linespoints pt 14 ps 0.5 title 'M=16'

set title 'd' font ",8" 
set logscale x
set xrange [1.5:*]
set xtics 2,2,16
set ytics auto
set logscale y
set key at 2,10000
plot 'F:\git\Wiser\output\brute-force.txt' using 2:3 with linespoints pt 6 ps 0.5 title 'M=2',\
     '' using 5:6 with linespoints pt 8 ps 0.5 title 'M=4',\
     '' using 8:9 with linespoints pt 10 ps 0.5 title 'M=8',\
     '' using 11:12 with linespoints pt 14 ps 0.5 title 'M=16'