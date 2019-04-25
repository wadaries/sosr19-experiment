set termoption dash
set style line 80 lt -1 lc rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"
set grid back linestyle 81
set border 3 back linestyle 80
set terminal pdfcairo size 2,4
set output '/Users/zhijia/git/Wiser/Gnuplot/pdf/evaluation_on_subsuming_and_subsumed_clause_size.pdf'
set multiplot layout 4, 1
#set bmargin 1;
#set tmargin 2;
#set lmargin 3;
set xtics nomirror font ", 8"# offset 0,0.5
set ytics nomirror font ", 8"# offset 0.5,0
#set key off
set key top left font ", 8"
#set ylabel "delay(ms)" font ",8" offset 4,0 
#set xlabel "size summation" font ",8" offset 0,1.5
#plot 'F:\git\Wiser\output\complexity_study.txt' using 2:1 with points pt 1 ps 0.2
#
#set bmargin 2;
set ylabel "delay(ms)"# font ",16"# offset 4,0 

set xlabel "random subsuming clause size"# font ",16"# offset 0,1.5
set title 'evaluation on random subsuming clause size'
plot '/Users/zhijia/git/Wiser/output/evalulation_on_subsuming_clause_size_random.txt' using 1:2 with points pt 0 ps 1 title 'fixed size = 1', '' using 1:3 with points pt 0 ps 1 title 'fixed size = 5', '' using 1:4 with points pt 0 ps 1 title 'fixed size = 10', '' using 1:5 with points pt 0 ps 1 title 'fixed size = 20'

set xlabel "random subsumed clause size"# font ",16"# offset 0,1.5
set title 'evaluation on random subsumed clause size'
plot '/Users/zhijia/git/Wiser/output/evalulation_on_subsumed_clause_size_random.txt' using 1:2 with points pt 0 ps 1 title 'fixed size = 1', '' using 1:3 with points pt 0 ps 1 title 'fixed size = 5', '' using 1:4 with points pt 0 ps 1 title 'fixed size = 10', '' using 1:5 with points pt 0 ps 1 title 'fixed size = 20'

set xlabel "MIRO subsuming clause size"# font ",16"# offset 0,1.5
set title 'evaluation on MIRO subsuming clause size'
plot '/Users/zhijia/git/Wiser/output/evalulation_on_subsuming_clause_size_MIRO.txt' using 1:2 with points pt 0 ps 1 title 'fixed size = 1', '' using 1:3 with points pt 0 ps 1 title 'fixed size = 5', '' using 1:4 with points pt 0 ps 1 title 'fixed size = 10', '' using 1:5 with points pt 0 ps 1 title 'fixed size = 20'

set xlabel "MIRO subsumed clause size"# font ",16"# offset 0,1.5
set title 'evaluation on MIRO subsumed clause size'
plot '/Users/zhijia/git/Wiser/output/evalulation_on_subsumed_clause_size_MIRO.txt' using 1:2 with points pt 0 ps 1 title 'fixed size = 1', '' using 1:3 with points pt 0 ps 1 title 'sfixed size = 5', '' using 1:4 with points pt 0 ps 1 title 'fixed size = 10', '' using 1:5 with points pt 0 ps 1 title 'fixed size = 20'
