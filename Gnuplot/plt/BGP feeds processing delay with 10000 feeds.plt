
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
set terminal pdfcairo size 2,1 font "Gill Sans,7" linewidth 1 rounded fontscale 1 
# set multiplot layout 2, 2
set lmargin at screen 0.13;
#set rmargin at screen 1.5;
set bmargin at screen 0.20;
set tmargin at screen 1.1;
set key bottom right font ",7" noopaque at 2.1,0.1 spacing 0.8 samplen 0.5 

set xtics nomirror offset 0,0.5
set ytics nomirror offset 0.5, 0
set ylabel "CDF" offset 2.5,0 font ",8"
set xlabel "millisecond" offset 0,1.3 font ",8"
# set title "BGP feeds processing delay"
# set xlabel "delay"
set yrange [0:1]



# default 5 by 3 (inches)
# set key opaque
# set xtics ("0.001" 0.001, "0.01" 0.01, "0.1" 0.1, "1" 1)
#set xtics (0.001,0.01,0.1,1)
#set xtics add ("Pi" 0.0314159) font "Gill Sans,7" offset 0
#set xtics border out scale 0.001

#set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/BGP_feeds_processing_10000_linear_sampled.pdf"
#set xrange [0:1]
#set xtics 0,0.1,1
#plot "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_default0pol_init_10000sampled.dat" using 2:1 title "default" with points pt 0 ps 0.2 lc 'red', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_miro5pol_init_10000sampled.dat" using 2:1 title "MIRO strawman" with points pt '<' ps 0.2 lc 'blue', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_wiser0pol_init_10000sampled.dat" using 2:1 title "Wiser strawman" with points pt 1 ps 0.2 lc rgb "#00A000"
#set xrange restore

#set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/BGP_feeds_processing_10000_logarithmic_sampled.pdf"
#set logscale x
#set xrange [:1]
#set xtics ("0.001" 0.001, "0.01" 0.01, "0.1" 0.1, "1" 1)
#plot "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_default0pol_init_10000sampled.dat" using 2:1 title "default" with points pt 0 ps 0.2 lc 'red', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_miro5pol_init_10000sampled.dat" using 2:1 title "MIRO strawman" with points pt '<' ps 0.2 lc 'blue', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_wiser0pol_init_10000sampled.dat" using 2:1 title "Wiser strawman" with points pt 1 ps 0.2 lc rgb "#00A000"
#unset logscale
#set xrange restore


set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/Residue_lin_sampled_indexed.pdf"
set xtics 0,0.5,2
# set xtics ("0" 0, "0.5" 0.5, "1" 1, "1.5" 1.5, "2" 2)
set xrange [0:2]
plot "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_miro_xpol_init_10000sampled.dat" using 2:1 title "insertion" with points pt 2 ps 0.2 lc 'red', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_miro_xpol_residue_10000sampled.dat" using 2:1 title "MIRO" with points pt 14 ps 0.2 lc 'blue', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_wiser_0pol_residue_10000sampled.dat" using 2:1 title "Wiser" with points pt 1 ps 0.2 lc rgb "#00A000","/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_combine_xpol_residue_10000sampled.dat" using 2:1 title "MIRO\\&Wiser" with points pt 10 ps 0.4 lc rgb "#F25900"

#set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/Residue_log_sampled_indexed.pdf"
#set logscale x
#set xtics autofreq
#set xrange [:2]
#plot "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_wiser_0pol_init_10000sampled.dat" using 2:1 title "insertion" with points pt 2 ps 0.2 lc 'red', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_miro_xpol_residue_10000sampled.dat" using 2:1 title "MIRO" with points pt 14 ps 0.2 lc 'blue', "/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_wiser_0pol_residue_10000sampled.dat" using 2:1 title "Wiser" with points pt 1 ps 0.2 lc rgb "#00A000","/Users/zhijia/git/Wiser/Gnuplot/dat/2914_1239_residue_combine_xpol_residue_10000sampled.dat" using 2:1 title "MIRO\\&Wiser" with points pt 10 ps 0.4 lc rgb "#F25900"

