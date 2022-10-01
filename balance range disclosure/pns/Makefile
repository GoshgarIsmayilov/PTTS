CXXFLAGS	+= -std=c++11 -Wall -Wextra -pedantic -lomp

# CXXFLAGS	+= -g -Og
CXXFLAGS	+= -O3

BINS		= pns-seq pns-seq-avx2 pns-seq-avx512 pns-omp pns-omp-avx2 pns-omp-avx512

.PHONY: all
all: $(BINS)

.PHONY: clean
clean:
	$(RM) $(BINS)

pns-seq: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-seq

pns-seq-avx2: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-seq-avx2 -DAVX2 -mavx2

pns-seq-avx512: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-seq-avx512 -DAVX512 -mavx512f

pns-omp: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-omp -DOMP -Xpreprocessor -fopenmp

pns-omp-avx2: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-omp-avx2 -DOMP_AVX2 -mavx2 -Xpreprocessor -fopenmp

pns-omp-avx512: pns.cpp
	$(CXX) $(CXXFLAGS) pns.cpp -o pns-omp-avx512 -DOMP_AVX512 -mavx512f -Xpreprocessor -fopenmp
