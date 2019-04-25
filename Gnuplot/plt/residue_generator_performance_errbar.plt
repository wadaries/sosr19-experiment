set output "/Users/zhijia/git/Wiser/Gnuplot/pdf/residue_generator_performance_errorbar.pdf"
set tmargin 0
set bmargin 2
set lmargin 8
set rmargin 1
#unset xtics
#unset ytics

set terminal pdfcairo size 3,20
set multiplot layout 20,1 title "residue generator performance\n" font ",12"
set ylabel "delay(ms)"
#set key autotitle column nobox samplen 1 noenhanced
# unset title
set auto x
set style data histogram
# We need to set lw in order for error bars to actually appear.
# We need to set lw in order for error bars to actually appear.
# Make the bars semi-transparent so that the errorbars are easier to see.
#set style fill solid 0.3
set style histogram errorbars gap 1
set style fill solid 0.5 border -1
set boxwidth 0.9
set xtics nomirror
set key top left opaque
#set bars front
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 2:($2-$3):($2+$3):xticlabels(1) title 'subsuming clause size = 1'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 4:($4-$5):($4+$5):xticlabels(1) title 'subsuming clause size = 2'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 6:($6-$7):($6+$7):xticlabels(1) title 'subsuming clause size = 3'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 8:($8-$9):($8+$9):xticlabels(1) title 'subsuming clause size = 4'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 10:($10-$11):($10+$11):xticlabels(1) title 'subsuming clause size = 5'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 12:($12-$13):($12+$13):xticlabels(1) title 'subsuming clause size = 6'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 14:($14-$15):($14+$15):xticlabels(1) title 'subsuming clause size = 7'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 16:($16-$17):($16+$17):xticlabels(1) title 'subsuming clause size = 8'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 18:($18-$19):($18+$19):xticlabels(1) title 'subsuming clause size = 9'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 20:($20-$21):($20+$21):xticlabels(1) title 'subsuming clause size = 10'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 22:($22-$23):($22+$23):xticlabels(1) title 'subsuming clause size = 11'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 24:($24-$25):($24+$25):xticlabels(1) title 'subsuming clause size = 12'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 26:($26-$27):($26+$27):xticlabels(1) title 'subsuming clause size = 13'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 28:($28-$29):($28+$29):xticlabels(1) title 'subsuming clause size = 14'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 30:($30-$31):($30+$31):xticlabels(1) title 'subsuming clause size = 15'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 32:($32-$33):($32+$33):xticlabels(1) title 'subsuming clause size = 16'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 34:($34-$35):($34+$35):xticlabels(1) title 'subsuming clause size = 17'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 36:($36-$37):($36+$37):xticlabels(1) title 'subsuming clause size = 18'
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 38:($38-$39):($38+$39):xticlabels(1) title 'subsuming clause size = 19'
#set xtic rotate by -45 scale 0
unset bmargin
set xlabel "subsumed clause size"
#set xtics nomirror
plot '/Users/zhijia/git/Wiser/output/subsuming_20_subsumed_20.txt' using 40:($40-$41):($40+$41):xticlabels(1) title 'subsuming clause size = 20'

#set tics scale 0# font ",8"
unset multiplot
 	

#


#set bmargin 10 
#plot '/Users/zhijia/git/Wiser/output/date_mins.tsv' using 2:xtic(1) ti col, '' u 3 ti col, '' u 4 ti col
#



