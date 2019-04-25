set termoption dash
set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 back linestyle 80
set terminal pdfcairo size 20,10
set output '/Users/zhijia/git/Wiser/Gnuplot/pdf/multiplication_eq_400.pdf'
set multiplot layout 2, 1
set bmargin 1;
set tmargin 0.5;
set lmargin 3;
set xtics nomirror #font ", 5" offset 0,0.5
set ytics nomirror #font ", 5" offset 0.5,0
set key off
#set ylabel "delay(ms)" font ",8" offset 4,0 
#set xlabel "size summation" font ",8" offset 0,1.5
#plot 'F:\git\Wiser\output\complexity_study.txt' using 2:1 with points pt 1 ps 0.2
#
set bmargin 2;
set ylabel "delay(ms)" font ",16" offset 4,0 
set xlabel "size multiplication" font ",16" offset 0,1.5
plot '/Users/zhijia/git/Wiser/output/multiplication_eq_400.txt' using 1:2 with points pt 0 ps 2

plot '/Users/zhijia/git/Wiser/output/eval_on_subsuming_clause_size.txt' using 1:2 with points pt 7 ps 1 title "subsumed size = 1", '' using 1:3 with points pt 7 ps 1 title "subsumed size = 5", '' using 1:4 with points pt 7 ps 1 title "subsumed size = 10", '' using 1:5 with points pt 7 ps 1 title "subsumed size = 20"#, '' using 1:6 with points pt 7 ps 1 title "subsumed size = 40"#, '' using 1:7 with points pt 7 ps 1 title "subsumed size = 32"
