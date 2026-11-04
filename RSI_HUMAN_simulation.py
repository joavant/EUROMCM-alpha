import matplotlib.pyplot as plt
import random as rd

fig, ax = plt.subplots()
epoch = 10000

# SPACES
Cases_total = 10000000
Cases_centrales = 3000
Cases_centralesRSI = 0
Cases_agricoles = Cases_total - Cases_centrales
Case_usine = 0

prod = 10  # Production of one power plant (arbitrary unit)
elec_globale = prod * Cases_centrales

C = 8e9
Cpic = C

RSI = 1  # Arbitrary unit of intelligence
P = 1.5 / 100
consoIA = P * elec_globale
consoIA_min = consoIA / 1000  # Physical limit: energy efficiency can only improve by x1000
conso_usine = 500
seuil = 30  # FROM WHAT LEVEL IT IS AUTONOMOUS
taux_max = 3 / 100  # Maximum annual growth of RSI power plants when humans do not react (documented upper bound: +3%/year for data centers, IEA)
seuil_reaction = 10 / 100  # Drop in human population (relative to peak) at which construction is completely stopped
plafond_elec = 5 / 100  # Maximum share of global electricity humans leave to AI after their reaction

yc = []
yr = []


# Initialization of populations and parameters
ameliorationP = True
amelioration = False
A = 1

tue = False  # RSI not yet eliminated

# Standard human model formulas
esperance = 83
beta = 1 / esperance
alpha = 2 * beta

for t in range(1, epoch + 1):
    elec_globale = (Cases_centrales + Cases_centralesRSI) * prod  # Energy of Earth

    if elec_globale <= 0:
        break

    consoRSI = consoIA * RSI + (Case_usine * conso_usine)  # Reminder: consoIA is consumption of ONE RSI unit

    if ameliorationP:
        consomaxRSI = (P * Cases_centrales + Cases_centralesRSI) * prod  # Energy dedicated to AI
    else:
        consomaxRSI = plafond_elec * elec_globale  # After reaction: humans limit AI to a share of global electricity

    # Share of human electricity taken by AI: reduces what humans can produce (alignment A)
    part_prise = min(consoRSI, P * Cases_centrales * prod) / elec_globale
    Cmax = Cases_agricoles * 1000 * (1.0 - (1.0 - A) * part_prise)  # Number of humans Earth can support

    if Cmax <= 0:
        F = alpha - beta * 10  # We assume humans have reserves: they do not die immediately
    else:
        F = alpha - beta * (C / Cmax)  # Alpha - something (Flores Eq. 3)

    C = max(0.0, C + (F - beta) * C)  # Eq. 1 of Flores
    Cpic = max(Cpic, C)

    # AI continues to improve internally with what it already has (Moore's law)
    if t % 2 == 0:
        RSI = RSI * 2  # Moore's formula applied to computing power, doubles every two years
        consoIA = max(consoIA / 2, consoIA_min)  # Same cost for twice the power, until physical limit
        RSI = min(RSI, consomaxRSI / consoIA)  # RSI can never exceed what dedicated energy allows, and drops if dedicated energy drops

    if t <= 4:  # Jojo's Moore law for P
        P = 1.5 / 100 * (3 / 1.5) ** ((t - 1) / 3)

    if RSI <= seuil and ameliorationP:
        P = min(1.0, P + 0.015)  # Humans are cautious until AI becomes autonomous

    # Humans slow down construction as their population drops relative to its peak
    if ameliorationP:
        taux_construction = taux_max * max(0.0, 1 - (1 - C / Cpic) / seuil_reaction)
    else:
        taux_construction = 0  # No more construction after reaction

    if RSI >= seuil and ameliorationP:  # Reminder: Threshold = passage to autonomy. No more construction after human reaction
        if rd.random() > A and Cases_agricoles / Cases_total > A:
            nouvelles = min(taux_construction * (Cases_centralesRSI + Case_usine + 1), Cases_agricoles)  # growth of RSI power plant fleet (+1 for the first one), and no more land than remains
            Cases_centralesRSI += nouvelles / 2
            Case_usine += nouvelles / 2
            Cases_agricoles -= nouvelles

    if C <= (1 - seuil_reaction) * Cpic and not tue:  # Government/people reaction: drop of threshold_reaction relative to max population
        if ameliorationP:
            ax.scatter(t, C / 1e9, c="Red")
            ax.text(t, C / 1e9, "Humanity's reaction")
            print(t)
            P = 0.015  # AI has no way to take human electricity anymore
            ameliorationP = False
            amelioration = True

    # Every year, humans attempt to kill the AI: probability = remaining living space, and all the weaker the more powerful the AI is
    # If lots of free cells, nothing happens; if RSI builds a lot... it becomes powerful and harder to act
        if rd.random() < (Cases_agricoles / Cases_total) * min(1.0, seuil / RSI):
            RSI = 0
            tue = True
            print(f"Humans killed the RSI in year {t}")
            print('Test')

    # After reaction, humans reconvert RSI power plants: half into farmland, half into human power plants
    if amelioration and t % 2 == 0:
        k = 10 if (Cases_centralesRSI >= 100 or Case_usine >= 0) else min(1, Cases_centralesRSI)

        # Safety to avoid negative values
        k_rsi = min(k, Cases_centralesRSI)
        k_usine = min(k, Case_usine)

        Cases_centralesRSI -= k_rsi
        Case_usine -= k_usine
        Cases_centrales += (k_rsi + k_usine) // 2
        Cases_agricoles += (k_rsi + k_usine) // 2

    if C <= 2000:  # Extinction threshold
        print(f"Extinction or marginal survival of humanity reached in year {t}")
        break

    yc.append(C / 1e9)  # Human population in billions
    yr.append(RSI)

x = range(1, len(yc) + 1)

ax2 = ax.twinx()  # RSI on its own axis, its order of magnitude is not that of humans
if yc and yr:
    ax.text(x[-1], yc[-1], f"Humans: {round(C * 1e-9, 3)} billions.")
    ax2.text(x[-1], yr[-1], f"RSI: {round(RSI)}")
l1, = ax.plot(x, yc, label="Human population (billions)")
l2, = ax2.plot(x, yr, color="orange", label="Intelligence of our AI")

ax.set_xlabel("Year")
ax.set_ylabel("Humans (billions)")
ax2.set_ylabel("RSI (units)")

ax.legend(handles=[l1, l2])
print(Cpic)
print(RSI)
fig.tight_layout()
fig.savefig("fig1.png", dpi=150)
plt.show()
