set termoption dash
set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border back 3 linestyle 80
set terminal pdfcairo size 2.35,1.2 font "Gill Sans,7" linewidth 1 rounded fontscale 1
set output 'Gnuplot/pdf/MIRO_historgram_errorbar.pdf'
set lmargin 5;
set rmargin 0;
set bmargin 2.5
set tmargin at screen 0.97;
set xtics nomirror offset 0,0.5
set ytics nomirror offset 0.5, 0
set logscale y
set ylabel "delay (ms)" font ",8" offset 2.5,0 
set xlabel "(size of MIRO policy 1, size of MIRO policy 2)" font ",8" offset 0,0.9
set key top left
set style fill solid border rgb "black"
set xrange [0:7]
set yrange [0:100]
#set datafile separator ","
set boxwidth 0.5
set xtics ("(2,4)" 1, "(2,16)" 2, "(2,64)" 3, "(2,2)" 4, "(4,2)" 5, "(8,2)" 6) offset 0,0.5
plot 'output/MIRO_policy_errorbar_reorder.txt' using 1:2:3 with boxerrorbars linecolor rgb "#808080",\
                                    '' using 1:(3*$2):(sprintf("%.3f", $2)) with labels,\
                                    '' using 4:5:6 with boxerrorbars linecolor rgb "#808080",\
                                    '' using 4:(3*$5):(sprintf("%.3f", $5)) with labels,\
                                    '' using 7:8:9 with boxerrorbars linecolor rgb "#808080",\
                                    '' using 7:(3*$8):(sprintf("%.3f", $8)) with labels,\
                                    '' using 10:11:12 with boxerrorbars fill pattern 2 linecolor 'black',\
                                    '' using 10:(3*$11):(sprintf("%.3f", $11)) with labels,\
                                    '' using 13:14:15 with boxerrorbars fill pattern 2 linecolor 'black',\
                                    '' using 13:(3*$14):(sprintf("%.3f", $14)) with labels,\
                                    '' using 16:17:18 with boxerrorbars fill pattern 2 linecolor 'black',\
                                    '' using 16:(2.5*$17):(sprintf("%.3f", $17)) with labels