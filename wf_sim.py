#!/usr/bin/env python
"""
Simulates genetic shifts over N generations of a Wright-Fisher population
"""

import argparse
import io
import numpy as np
import random

class Population:
    def __init__(self, N = 10, f = 0.2, with_np = False, outfile = None):
        self.N = N
        self.f = f
        self.Nf = round(N * f)
        self.with_np = with_np
        self.outfile = outfile

        if with_np == True:
            self.pop = np.repeat([0, 1], [N - self.Nf, self.Nf])
        else:
            self.pop = ([0] * (N - self.Nf)) + ([1] * self.Nf)

    def step(self, ngens=10):
        results = []
        
        for i in range(ngens):
            if self.with_np:
                self.pop[:] = self.pop[np.random.randint(0, high=self.N, size=self.N)]
            else:
                self.pop = random.choices(self.pop, k=self.N)
            
            if self.outfile:
                entry = f"Generation {i+1} (frequency of derived = {sum(self.pop)/self.N})\n {self.pop}\n"
                results.append(entry)
        
        if self.outfile:
            with open(self.outfile, "a") as f:
                f.writelines(results)
        
        return self.pop

    def __repr__(self):
        return f"Population(N={self.N}, f={self.f})"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-N", help = "Size of population to simulate", 
                        dest = 'N', type = int, default = 10)
    parser.add_argument("-f", help = "Frequency of derived alleles in initial population", 
                        dest = 'f', type = float, default = 0.2)
    parser.add_argument("-g", "--ngens", help = "Number of generations to simulate", 
                        dest = 'ngens', type = int, default = 10)
    parser.add_argument("-np", "--with_np", 
                        help = "Optional: run simulations using numpy arrays instead of lists (faster for larger populations/more generations)", 
                        action = "store_true")
    parser.add_argument("-v", "--verbose", help = "Increase output verbosity", 
                        action = "store_true")
    parser.add_argument("-o", "--outfile", 
                       help = "Path to file. If None, results will not be saved.",
                       dest = "outfile", type = str, default=None)
    parser.add_argument("-j", "--justification", 
                       help = "Prints justification for values stored in outfile",
                       action = "store_true")
    
    args = parser.parse_args()

    pop = Population(N = args.N, f = args.f, with_np = args.with_np, outfile = args.outfile)

    if args.verbose:
        print(f"The initial population consists of {args.N} individuals, {pop.Nf} of which carry the derived allele:")
        print(f"{pop.pop}\n")
        if args.with_np:
            print("An array-based method will be used. Beginning simulation...\n")
        else: 
            print("A list-based method will be used. Beginning simulation...\n")

    final = pop.step(ngens = args.ngens)
    
    if args.verbose:
        print(f"After {args.ngens} generations, the population is:")
        print(f"{final}\n")
        print("And they all lived happily ever after. Goodbye.")
    else:
        print(f"{final}")

    if args.outfile:
        print(f"Results written to {args.outfile}")

    if args.justification:
        print(f"The values stored in {args.outfile} include the generation number, the frequency of the derived allele, and the population at that step. These values were chosen to provide a snapshot of the results at that step, while ensuring the file was still easy for the user to parse and understand. A simpler file could be created that only reported the generation, frequencies, and counts, without the actual population; however, given the relatively simple format of the population, it seemed trivial to include it, as well. Future versions could pass that option off to the user.")

