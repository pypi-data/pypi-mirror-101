alias gen="python3.9 ./iterator/randgen.py"

# Generiamo le matrici triangolari superiori
gen -nc=5 -nr=5 -t=1 -nm=10000 > ./matrix/triangular/superior/sup_5_5_10000.mtx
gen -nc=10 -nr=10 -t=1 -nm=1000 > ./matrix/triangular/superior/sup_10_10_1000.mtx
gen -nc=50 -nr=50 -t=1 -nm=100 > ./matrix/triangular/superior/sup_50_50_100.mtx
gen -nc=100 -nr=100 -t=1 -nm=10 > ./matrix/triangular/superior/sup_100_100_10.mtx

# Generiamo le matrici triangonali inferiori
gen -nc=5 -nr=5 -t=2 -nm=10000 > ./matrix/triangular/inferior/inf_5_5_10000.mtx
gen -nc=10 -nr=10 -t=2 -nm=1000 > ./matrix/triangular/inferior/inf_10_10_1000.mtx
gen -nc=50 -nr=50 -t=2 -nm=100 > ./matrix/triangular/inferior/inf_50_50_100.mtx
gen -nc=100 -nr=100 -t=2 -nm=10 > ./matrix/triangular/inferior/inf_100_100_10.mtx

# Generiamo le matrici diagonali
gen -nc=5 -nr=5 -t=3 -nm=10000 > ./matrix/diagonal/diagonal/diag_5_5_10000.mtx
gen -nc=10 -nr=10 -t=3 -nm=1000 > ./matrix/diagonal/diagonal/diag_10_10_1000.mtx
gen -nc=50 -nr=50 -t=3 -nm=100 > ./matrix/diagonal/diagonal/diag_50_50_100.mtx
gen -nc=100 -nr=100 -t=3 -nm=10 > ./matrix/diagonal/diagonal/diag_100_100_10.mtx

# Generiamo le matrici identità
gen -nc=5 -nr=5 -t=4 -nm=10000 > ./matrix/diagonal/identity/id_5_5_10000.mtx
gen -nc=10 -nr=10 -t=4 -nm=1000 > ./matrix/diagonal/identity/id_10_10_1000.mtx
gen -nc=50 -nr=50 -t=4 -nm=100 > ./matrix/diagonal/identity/id_50_50_100.mtx
gen -nc=100 -nr=100 -t=4 -nm=10 > ./matrix/diagonal/identity/id_100_100_10.mtx

# Generiamo le matrici nulle
gen -nc=5 -nr=5 -t=5 -nm=10000 > ./matrix/simple/null/null_5_5_10000.mtx
gen -nc=10 -nr=10 -t=5 -nm=1000 > ./matrix/simple/null/null_10_10_1000.mtx
gen -nc=50 -nr=50 -t=5 -nm=100 > ./matrix/simple/null/null_50_50_100.mtx
gen -nc=100 -nr=100 -t=5 -nm=10 > ./matrix/simple/null/null_100_100_10.mtx

# Generiamo le matrici colonna
gen -nr=5 -t=6 -nm=10000 > ./matrix/single/columns/col_5_5_10000.mtx
gen -nr=10 -t=6 -nm=1000 > ./matrix/single/columns/col_10_10_1000.mtx
gen -nr=50 -t=6 -nm=100 > ./matrix/single/columns/col_50_50_100.mtx
gen -nr=100 -t=6 -nm=10 > ./matrix/single/columns/col_100_100_10.mtx

# Generiamo le matrici vettore
gen -nc=5 -t=7 -nm=10000 > ./matrix/single/rows/row_5_5_10000.mtx
gen -nc=10 -t=7 -nm=1000 > ./matrix/single/rows/row_10_10_1000.mtx
gen -nc=50 -t=7 -nm=100 > ./matrix/single/rows/row_50_50_100.mtx
gen -nc=100 -t=7 -nm=10 > ./matrix/single/rows/row_100_100_10.mtx

# Generiamo le matrici rettangolari
gen -nc=10 -nr=5 -t=8 -nm=10000 > ./matrix/simple/rectangular/rect_10_5_10000.mtx
gen -nc=5 -nr=10 -t=8 -nm=10000 > ./matrix/simple/rectangular/rect_5_10_10000.mtx
gen -nc=7 -nr=81 -t=8 -nm=1000 > ./matrix/simple/rectangular/rect_7_81_1000.mtx
gen -nc=81 -nr=7 -t=8 -nm=1000 > ./matrix/simple/rectangular/rect_81_7_1000.mtx
gen -nc=50 -nr=51 -t=8 -nm=100 > ./matrix/simple/rectangular/rect_50_51_100.mtx
gen -nc=51 -nr=50 -t=8 -nm=100 > ./matrix/simple/rectangular/rect_51_50_100.mtx
gen -nc=70 -nr=100 -t=8 -nm=10 > ./matrix/simple/rectangular/rect_70_100_10.mtx
gen -nc=100 -nr=70 -t=8 -nm=10 > ./matrix/simple/rectangular/rect_100_70_10.mtx

# Generiamo le matrici anti-diagonali
gen -nc=5 -nr=5 -t=9 -nm=10000 > ./matrix/diagonal/antidiagonal/adiag_5_5_10000.mtx
gen -nc=10 -nr=10 -t=9 -nm=1000 > ./matrix/diagonal/antidiagonal/adiag_10_10_1000.mtx
gen -nc=50 -nr=50 -t=9 -nm=100 > ./matrix/diagonal/antidiagonal/adiag_50_50_100.mtx
gen -nc=100 -nr=100 -t=9 -nm=10 > ./matrix/diagonal/antidiagonal/adiag_100_100_10.mtx