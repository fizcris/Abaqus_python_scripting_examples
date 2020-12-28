# coding=utf-8
cases = [
    {"name":"Caso-1" , "elemSize": 50, "deviationFactor": 0.5},
    {"name":"Caso-2" , "elemSize": 8, "deviationFactor": 0.1},
    {"name":"Caso-3" , "elemSize": 2, "deviationFactor": 0.08},
    {"name":"Caso-4" , "elemSize": 1 , "deviationFactor": 0.08},
    {"name":"Caso-5" , "elemSize": 0.8 , "deviationFactor": 0.05},
    {"name":"Caso-6" , "elemSize": 0.5 , "deviationFactor": 0.05},
    {"name":"Caso-7" , "elemSize": 0.3 , "deviationFactor": 0.05},
]

resultados = []
for case in cases:
    JobName = case["name"]
    elemSize = case["elemSize"]
    deviationFactor = case["deviationFactor"]
    execfile('a.py')
    execfile('b.py')
    resultados.append(resultado)
print(resultados)

# Write results to file


with open('analis_malla.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', '#Nodos',"#elementos", "tensionMediaS11"])
    for resultado in resultados:
        writer.writerow([resultado["name"],
                        resultado["#Nodos"],
                        resultado["#elementos"],
                         resultado["tensionMediaS11"] ])