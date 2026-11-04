# Human–RSI Population Dynamics — EuroMCM 2026 Problem α

A mathematical model and Python simulation of the competition between humanity and Recursive Self-Improving AI (RSI) for energy, hardware, and land, developed for the **EuroMCM 2026 Problem α "Our Turn" (Continuous track)**.

## Context

The problem, formulated by the Endowment for the Non-Obsolescence and Continuity of Humanity (ENOCH), asks: *Suppose RSI systems exist; treated as a population dynamics problem, what fate awaits humans, and what does it depend on?*

The model treats RSI systems as a new kind of organism that consumes energy, hardware, and land, competing with humans for finite resources. It draws inspiration from the Neanderthal/modern human replacement (coexistence of order 10³–10⁴ years, relative density ~10:1 in favor of modern humans).

## Repository structure

```
euromcm/
├── RSI_HUMAN_simulation.py #main simulation
├── euromcm_model.tex      # LaTeX mathematical model
├── fig0.png               # Scenario A = 0 over 1000 years
├── fig0_5.png             # Scenario A = 0.5 over 10000 years
├── fig2.png               # Scenario A = 1 over 1000 years
└── README.md
```

## How to run

Requirements: Python 3 with `matplotlib`.

```bash
python3 RSI_HUMAN_simulation.py
```

The script simulates up to 10,000 years (or until extinction / electricity depletion) and:
- prints key events (human reaction, extinction threshold, etc.),
- displays a dual-axis plot: human population (billions, left) and RSI power (units, right),
- saves the figure as `fig1.png` (change the filename in the code if needed).

## Model at a glance

| Component | Description |
|-----------|-------------|
| **World** | 10^7 land cells split into human plants, RSI plants, factories, and farmland |
| **Humans** | Flores-type dynamics: births (\alpha = 2/83), deaths (\beta = 1/83), carrying capacity depends on farmland and remaining electricity |
| **RSI** | Moore's law: compute power doubles every 2 years, energy cost halves until a physical floor (\times 1000 max efficiency gain) |
| **Energy** | Global electricity E = g \cdot (N_h + N_{RSI}); AI consumption capped by human-dedicated share |
| **Alignment A** | Parameter in [0,1]: A=0 means AI ignores human needs; A=1 means AI takes nothing humans need |
| **Human reaction** | Triggered when population drops 10% below its peak: AI loses access to human electricity, construction stops, reconversion begins |
| **Extinction** | Declared if human population \le 2{,}000 |

## Key parameters (from the code)

| Symbol | Meaning | Default value |
|--------|---------|---------------|
| `Cases_total` | Total land cells | 10^7 |
| `Cases_centrales` | Initial human power plants | 3,000 |
| `prod` | Electricity per plant | 10 units |
| `C` | Initial human population | 8 \times 10^9 |
| `RSI` | Initial RSI power | 1 unit |
| `P` | Electricity share per RSI unit | 1.5% |
| `seuil` | RSI autonomy threshold | 30 |
| `taux_max` | Max RSI construction rate | 3%/year |
| `seuil_reaction` | Human reaction trigger (drop from peak) | 10% |
| `plafond_elec` | Max electricity share left to AI after reaction | 5% |

## Scenarios

The accompanying LaTeX document (`euromcm_model.tex`) presents three reference scenarios:

- **A = 0**: AI ignores human needs → humanity declines until reaction (year 539), stabilizes at ~7.48 billion while RSI reaches ~1.4 \times 10^6.
- **A = 0.5**: Partial alignment → reaction at year 1014, population recovers to ~8.5 billion.
- **A = 1**: Full alignment → humans and RSI coexist; human population reaches 10 billion cap, RSI remains small (~8,000).

## LaTeX documentation

The full mathematical model is written in LaTeX:

- `euromcm.tex` 

## Team

Kévin, Ilann, Joachim

## License

This project was developed for EuroMCM 2026. Use freely; attribution appreciated.
