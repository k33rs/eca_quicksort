set terminal postscript color
set style data linespoints

set logscale x 2
set logscale y 10
set nokey
set xtics (1, 2, 4, 8, 16, 32)

set title "Distributed Quickhull"
set xlabel "Processes (p)"

set key on

set ylabel "Execution Time (sec)"
set output "charts/gpStrongTime.ps"
plot [1:33] 'plot.data' index 0 using 1:2 title "N=10^2" with linespoints ls 1, \
    'plot.data' index 1 using 1:2 title "N=10^3" with linespoints ls 2, \
    'plot.data' index 2 using 1:2 title "N=10^4" with linespoints ls 3, \
    'plot.data' index 3 using 1:2 title "N=10^5" with linespoints ls 4
