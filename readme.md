[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Traveling Salesman Problem — Hill Climbing with 2-opt/Insertion and Size-Aware Sampling

This repository implements and documents a simple yet powerful baseline for the Euclidean Traveling Salesman Problem (TSP), using nearest-neighbor initialization, steepest-ascent hill climbing, and 2-opt/insertion neighborhood search.  
For small instances (n < 150), the neighborhoods are fully enumerated; for larger instances, a sampled variant is used.  
The companion report in `docs/report.pdf` presents detailed experiments across six TSPLIB benchmarks.

---

## Results Summary (from report)

| Instance  | Optimum | Swap  | 2-opt | Insertion |
|-----------|---------|-------|-------|-----------|
| eil51     | 426     | 459   | 429   | 444       |
| berlin52  | 7542    | 8088  | 7657  | 7895      |
| ch150     | 6528    | 6937  | 6854  | 7176      |
| kroA200   | 29368   | 33097 | 32695 | 34695     |
| pr1002    | 259045  | 313853| 312249| 315234    |
| nrw1379   | 56638   | 68924 | 68433 | 68766     |

---

## Detailed Restart-Level Results (Table 1 from report)

| Instance | Method  | Restarts | Best     | Optimum | Gap (%) |
|-----------|----------|-----------|----------|----------|---------|
| **eil51** | Swap | 100 | 467 | 426 | 9.62 |
|  | Swap | 200 | 459 | 426 | 7.75 |
|  | 2-opt | 100 | 429 | 426 | 0.70 |
|  | Insert | 100 | 444 | 426 | 4.23 |
| **berlin52** | Swap | 100 | 8088 | 7542 | 7.24 |
|  | Swap | 200 | 8088 | 7542 | 7.24 |
|  | 2-opt | 100 | 7657 | 7542 | 1.53 |
|  | Insert | 100 | 7937 | 7542 | 5.24 |
|  | 2-opt | 200 | 7657 | 7542 | 1.53 |
|  | Insert | 200 | 7895 | 7542 | 4.68 |
| **ch150** | Swap | 20 | 6937 | 6528 | 6.27 |
|  | Swap | 30 | 6937 | 6528 | 6.27 |
|  | 2-opt | 20 | 6854 | 6528 | 4.99 |
|  | Insert | 20 | 7176 | 6528 | 9.93 |
| **kroA200** | Swap | 20 | 33097 | 29368 | 12.70 |
|  | Swap | 20 | 33973 | 29368 | 15.69 |
|  | Swap | 30 | 33792 | 29368 | 15.07 |
|  | 2-opt | 20 | 32695 | 29368 | 11.33 |
|  | 2-opt | 30 | 32989 | 29368 | 12.33 |
|  | Insert | 20 | 34695 | 29368 | 18.12 |
| **pr1002** | Swap | 30 | 313853 | 259045 | 21.15 |
|  | Swap | 20 | 314532 | 259045 | 21.43 |
|  | 2-opt | 30 | 312249 | 259045 | 20.53 |
|  | 2-opt | 20 | 313210 | 259045 | 20.91 |
|  | Insert | 30 | 315234 | 259045 | 21.69 |
|  | Insert | 20 | 316781 | 259045 | 22.29 |
| **nrw1379** | Swap | 20 | 69035 | 56638 | 21.89 |
|  | Swap | 30 | 68924 | 56638 | 21.70 |
|  | 2-opt | 20 | 68748 | 56638 | 21.39 |
|  | 2-opt | 30 | 68433 | 56638 | 20.81 |
|  | Insert | 20 | 68885 | 56638 | 21.61 |
|  | Insert | 30 | 68766 | 56638 | 21.40 |

---

## Usage

```bash
python src/tsp_hillclimb.py data/tsplib/eil51.tsp
python src/tsp_hillclimb.py data/tsplib/ch150.tsp 200
```

---

## Design Notes

- TSPLIB-conformant integer-rounded Euclidean distances  
- Size-aware full/sampled neighborhood strategy  
- Deterministic reproducibility via random seed  

---

## Repository Layout

```
tsp-hillclimb/
├── src/
│   └── tsp_hillclimb.py
├── docs/
│   └── report.pdf
├── data/
│   ├── tsplib/
│   └── results/
├── tests/
│   └── test_smoke.py
├── requirements.txt
└── README.md
```

---

## License

MIT License
