
reset

set termoption dash

set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 back linestyle 80

set style line 1 lt rgb "#A00000" lw 1 pt 1 ps 1
set style line 2 lt rgb "#00A000" lw 1 pt 6 ps 1
set style line 3 lt rgb "#5060D0" lw 1 pt 2 ps 1
set style line 4 lt rgb "#F25900" lw 1 pt 9 ps 1

set style line 11 lt -1 lc rgb "#A00000" lw 2 
set style line 12 lt -1 lc rgb "#00A000" lw 2
set style line 13 lt -1 lc rgb "#5060D0" lw 2
set style line 14 lt 1 lc rgb "#F25900" lw 2
set terminal pdfcairo size 2,1.2 font "Gill Sans,7" linewidth 1 rounded fontscale 1
set output 'Gnuplot/pdf/MIRO_Wiser_CDF.pdf'
set lmargin at screen 0.13;
set rmargin at screen 1;
set bmargin 2.5
set tmargin at screen 0.97;
set logscale x
set xtics nomirror offset 0,0.5
set ytics nomirror offset 0.5, 0
# set key top left font ",7"
set key at 7,1 font ",7"
set ylabel "CDF" offset 2.5,0  font ",8"
set xlabel "delay (ms)" offset 0,0.9 font ",8"
# set xtics 0,0.5,2
# set xtics ("0" 0, "0.2" 0.2, "0.5" 0.5, "8" 8)
#plot 'output/MIRO_Wiser_CDF.txt' using 2:1 title "M=2" with points pt 1 ps 0.2 lc 'red', '' using 3:1 title "M=4" with points pt 2 ps 0.2 lc 'blue', '' using 4:1 title "M=8" with points pt 14 ps 0.2 lc rgb "#00A000"

set logscale x
set xrange [0:20]
set xtics ("0.266" 0.266, "0.705" 0.705, "10.524" 10.524)
plot 'output/MIRO_Wiser_CDF.txt' using 2:1 title "M=2" with points pt 1 ps 0.5 lc 'red', '' using 3:1 title "M=4" with points pt 2 ps 0.5 lc 'blue', '' using 4:1 title "M=8" with points pt 4 ps 0.5 lc rgb "#00A000"

