
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
set terminal pdfcairo size 1.7,1 font "Gill Sans,7" linewidth 1 rounded fontscale 1 
set lmargin at screen 0.15;
#set rmargin at screen 1.7;
set bmargin at screen 0.25;
set tmargin at screen 0.95;

# set xtics nomirror offset 0,0.5
# set ytics nomirror offset 0.5, 0

set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/residue_generator_performance.pdf"
set xtics nomirror offset 0,0.5
set ytics nomirror offset 0.5, 0
# set key top left font ",7"
set key at 16,30 font ",7"
#set ylabel "delay (millisecond)" offset 2.5,0 font ",8"
#set xlabel "predicate number in each clause" offset 0,1.3 font ",8"
set ylabel "delay (millisecond)" offset 2,0 font ",8"
set xlabel "# predicates" offset 0,1.3 font ",8"
# set xtics 0,0.5,2
# set xtics ("0" 0, "0.5" 0.5, "1" 1, "1.5" 1.5, "2" 2)
set xrange [0:20]
plot "/Users/zhijia/git/Wiser/output/predicate_number2delay.txt" using 1:2 title "with 5 args" with points pt 1 ps 0.2 lc 'red', "" using 1:3 title "with 10 args" with points pt 2 ps 0.2 lc 'blue', "" using 1:4 title "with 20 args" with points pt 14 ps 0.2 lc rgb "#00A000"

set key default
set key bottom right opaque
set xrange [0:1.5]
set ylabel "CDF" offset 2.5,0 font ",8"
set xlabel "millisecond" offset 0,1.3 font ",8"
# set title "BGP feeds processing delay"
# set xlabel "delay"
set yrange [0:1]
set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/residue_generator_MIRO_CDF.pdf"
# set xtics 0,0.5,2
# set xtics ("0" 0, "0.5" 0.5, "1" 1, "1.5" 1.5, "2" 2)
plot "/Users/zhijia/git/Wiser/output/residue_generator_MIRO_CDF.txt" using 2:1 title "1 condition" with points pt 2 ps 0.2 lc 'red', '' using 3:1 title "3 conditions" with points pt 14 ps 0.2 lc 'blue', '' using 4:1 title "5 conditions" with points pt 1 ps 0.2 lc rgb "#00A000"


