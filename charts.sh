#!/bin/bash
cd data
rm -f *.png
gnuplot <<EOF
set ylabel "Seconds"
set xlabel "File Size (bytes)"
set title "Seconds To Verify Files by File Size"
set logscale x
set logscale y
set xrange [1:10.5e10]
set yrange [:1000]
unset key
set terminal png size 640,640 font ",15"
set output 'verify.png'
plot 'verify.tsv' using 1:2 w points t 'Seconds to Verify' lw 1 lc rgb "black"
set terminal postscript eps solid size 3.5,3 enhanced color font 'Helvetica,15'
set output '../paper/verify.eps'
replot
EOF
gnuplot <<EOF
set ylabel "Number of Files"
set xlabel "File Size (bytes)"
set title "Number of Files in Archive by File Size"
set logscale x
set logscale y
set style fill solid
set boxwidth 0.5
set xrange [0.5:10.5e10]
unset key
set terminal png size 640,640 font ",15"
set output 'files.png'
plot 'FileSizes.tsv' using 3:4 w boxes t 'Number of Files' lw 1 lc rgb "black"
set terminal postscript eps solid size 3.5,3 enhanced color font 'Helvetica,15'
set output '../paper/files.eps'
replot
EOF
gnuplot <<EOF
set ylabel "KB per Second"
set xlabel "File Size (bytes)"
set title "Average Transfer Speed by File Size"
set logscale x
set xrange [1:10.5e10]
unset key
set terminal png size 640,640 font ",15"
set output 'bps.png'
n = 1024
plot 'speed.tsv' using 1:((\$2)/n) w points t 'Bytes per Second' lw 1 lc rgb "black"
set terminal postscript eps solid size 3.5,3 enhanced color font 'Helvetica,15'
set output '../paper/bps.eps'
replot
EOF
gnuplot <<EOF
set ylabel "Fraction of Communication Time Transferring Data"
set xlabel "File Size"
set title "Efficiency of File Transfers by File Size"
set logscale x
set xrange [1:10.5e10]
set yrange [0:1.05]
unset key
set terminal png size 640,640 font ",15"
set output 'busyness.png'
plot 'busyness.tsv' using 1:2 w points t 'Transfer-to-Total Time' lw 1 lc rgb "black"
set terminal postscript eps solid size 3.5,3 enhanced color font 'Helvetica,15'
set output '../paper/busyness.eps'
replot
EOF
cd ..
