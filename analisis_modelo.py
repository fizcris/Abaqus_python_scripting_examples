# coding=utf-8
case = {"name": "Caso-5", "elemSize": 0.8, "deviationFactor": 0.05}

elemSize = case["elemSize"]
deviationFactor = case["deviationFactor"]

# mYoung en MPA
# fuerza en N
simulaciones = [{"name": "Sim-1", "mYoung": 215220.00, "mPoiss": 0.317, "fuerza": 14.88},
                {"name": "Sim-2", "mYoung": 215220.00, "mPoiss": 0.3432, "fuerza": 14.88},
                {"name": "Sim-3", "mYoung": 206780.00, "mPoiss": 0.3432, "fuerza": 14.88},
                {"name": "Sim-4", "mYoung": 206780.00, "mPoiss": 0.317, "fuerza": 14.88},
                {"name": "Sim-5", "mYoung": 215220.00, "mPoiss": 0.317, "fuerza": 14.84},
                {"name": "Sim-6", "mYoung": 215220.00, "mPoiss": 0.3432, "fuerza": 14.84},
                {"name": "Sim-7", "mYoung": 206780.00, "mPoiss": 0.317, "fuerza": 14.84},
                {"name": "Sim-8", "mYoung": 206780.00, "mPoiss": 0.3432, "fuerza": 14.84},
                {"name": "Sim-9", "mYoung": 211000.00, "mPoiss": 0.33, "fuerza": 14.86}
                ]

resultados = []
for simulacion in simulaciones:
    JobName = simulacion["name"]
    mYoung = simulacion["mYoung"]
    mPoiss = simulacion["mPoiss"]
    fuerza = simulacion["fuerza"]
    execfile('a.py')
    execfile('b.py')
    resultado.update(simulacion)
    resultados.append(resultado)

print(resultados)

# Write results to file


with open('analis_modelo.csv', 'w', ) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', '#Nodos', "#elementos", "mYoung", "mPoiss", "fuerza", "tensionMediaS11"])
    for resultado in resultados:
        writer.writerow([resultado["name"],
                         resultado["#Nodos"],
                         resultado["#elementos"],
                         resultado["mYoung"],
                         resultado["mPoiss"],
                         resultado["fuerza"],
                         resultado["tensionMediaS11"]])