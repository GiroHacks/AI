import csv
import pickle
from pprint import pprint
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data ####################################################
with open('skills.csv') as fin:
    raw_skills = list(csv.reader(fin))[1:]
    print(f"Raw skills = {len(raw_skills)}")

with open('views_leads.csv') as fin:
    raw_jobs = list(csv.reader(fin))[1:]
    print(f"Raw jobs = {len(raw_jobs)}")
################################################################

KNC_GROUPS = 30

# WARNING: Full dataset can take up more than 64GB of RAM
#          You've been warned.
DATASET_MAX_SIZE = 30000

#
# WARNING: DEBUG TEST HACK
#
raw_jobs = raw_jobs[:DATASET_MAX_SIZE]
#
#
#

massilla_powerup_skills = [
    ('VENTAS', 'VENTAS'),
    ('GESTION', 'GESTION'),
    ('ATENCION AL CLIENTE', 'SOPORTE'),
    ('COMERCIAL', 'VENTAS'),
    ('MANTENIMIENTO', 'SOPORTE TECNICO'),
    ('JAVA', 'DESARROLLO BACKEND'),
    ('CALIDAD', 'I+D'),
    ('NEGOCIACION', 'VENTAS'),
    ('TELECOMUNICACIONES', 'IT'),
    ('ADMINISTRACION', 'ADMINISTRACION'),
    ('SEGUROS', 'VENTAS'),
    ('ANALISIS', 'ADMINISTRACION'),
    ('INDUSTRIAL', 'INGENIERIA'),
    ('ELECTRICIDAD', 'SOPORTE TECNICO'),
    ('SQL', 'DESAROLLADOR DE BASES DE DATOS'),
    ('SEGURIDAD', 'IT'),
    ('DOCUMENTACION', 'ADMINISTRACION'),
    ('INFORMATICA', 'IT'),
    ('CONTABILIDAD', 'ADMINISTRACION'),
    ('MARKETING', 'VENTAS'),
    ('ADMINISTRATIVO', 'ADMINISTRACION'),
    ('ENERGIA', 'INGENIERIA'),
    ('LOGISTICA', 'VENTAS'),
    ('INGLES', 'IDIOMAS'),
    ('SAP', 'DESAROLLO BACKEND'),
    ('MICROSOFT OFFICE', 'ADMINISTRACION'),
    ('CONSULTORIA', 'ADMINISTRACION'),
    ('CAPTACION DE CLIENTES', 'RECURSOS HUMANOS'),
    ('VEHICULOS', 'VENTAS'),
    ('ASESOR', 'VENTAS'),
    ('MECANICA', 'INGENIERIA'),
    ('SOFTWARE', 'DESAROLLO FULL STACK'),
    ('FACTURACION', 'ADMINISTRACION'),
    ('TELEMARKETING', 'VENTAS'),
    ('LINUX', 'DEVOPS'),
    ('VENTA Y ATENCION AL CLIENTE', 'VENTAS'),
    ('CRM', 'DISENYO'),
    ('JAVASCRIPT', 'DESAROLLO FRONTEND'),
    ('MICROSOFT EXCEL', 'ADMINISTRACION'),
    ('ATENCION TELEFONICA', 'SOPORTE'),
    ('MAQUINARIA', 'SOPORTE TECNICO'),
    ('ORIENTACION', 'ADMINISTRACION'),
    ('OFIMATICA', 'ADMINISTRACION'),
    ('GESTION DE EQUIPOS', 'ADMINISTRACION'),
    ('NET', 'DESAROLLO BACKEND'),
    ('AGENTE COMERCIAL', 'VENTAS'),
    ('LIDERAZGO', 'ADMINISTRACION'),
    ('PROMOTOR', 'VENTAS'),
    ('RECURSOS HUMANOS', 'RECURSOS HUMANOS'),
    ('TELEFONIA', 'SOPORTE TECNICO'),
    ('AUTOCAD', 'ARQUITECTURA'),
    ('SPRING', 'DESAROLLO BACKEND'),
    ('VENTA', 'VENTAS'),
    ('ALIMENTACION', 'VENTAS'),
    ('AGENTES', 'ADMINISTRACION'),
    ('ELECTRONICA', 'INGENIERIA'),
    ('PYTHON', 'DESAROLLO FULL STACK'),
    ('MODA', 'MODA'),
    ('FACTURAS', 'ADMINISTRACION'),
    ('CONSTRUCCION', 'INGENIERIA'),
    ('TELEOPERADOR', 'VENTAS'),
    ('CONTRATOS', 'ADMINISTRACION'),
    ('REPARTIDOR', 'VENTAS'),
    ('PRESUPUESTOS', 'VENTAS'),
    ('ORACLE', 'DESAROLLADOR DE BASES DE DATOS'),
    ('FINANZAS', 'VENTAS'),
    ('TECNICAS DE VENTA', 'VENTAS'),
    ('GIT', 'DESAROLLADOR'),
    ('COMPRAS', 'VENTAS'),
    ('GESTION DE INCIDENCIAS', 'ADMINISTRACION'),
    ('REDES SOCIALES', 'ADMINISTRACION'),
    ('PREPARACION DE PEDIDOS', 'VENTAS'),
    ('MANTENIMIENTO PREVENTIVO', 'SOPORTE TECNICO'),
    ('GESTION COMERCIAL', 'ADMINISTRACION'),
    ('DELIVERY', 'VENTAS'),
    ('PREVENCION DE RIESGOS LABORALES', 'RECURSOS HUMANOS'),
    ('GESTION DE PROYECTOS', 'ADMINISTRACION'),
    ('SOLDADURA', 'SOPORTE TECNICO'),
    ('REPARTIDORA', 'VENTAS'),
    ('ENFERMERIA', 'SANIDAD'),
    ('ANGULAR', 'DESAROLLADOR FRONT END'),
    ('SQL SERVER', 'DESAROLLADOR DE BASES DE DATOS'),
]

# Process efficient data types #################################
jobs_ids   = set(j[0] for j in raw_jobs)
skills_ids = set(j[0] for j in raw_skills)
match_ids  = jobs_ids.intersection(skills_ids)
print(len(match_ids))
################################################################

# Clean up unnecessary data
jobs   = [j for j in raw_jobs if j[0] in match_ids]
skills = [s for s in raw_skills if s[0] in match_ids]

# sname = {s[1]: s[0] for s in skills}
# len(sname.keys())

# Calculate idnames
idnames = {}
for s in skills:
    if not s[0] in idnames:
        idnames[s[0]] = []
    idnames[s[0]].append(s[1])

print(len(idnames))

# Calculate jobskills = [['SKILL1', 'SKILL2'], ...]
jobskills = [set(idnames[j[0]]) for j in jobs if j[0] in idnames]

freqskills={}
for js in jobskills:
    for jjs in js:
        if jjs not in freqskills:
            freqskills[jjs] = 0
        freqskills[jjs] += 1

print(len(idnames))

# Calculate jobskills = [['SKILL1', 'SKILL2'], ...]
jobskills = [set(idnames[j[0]]) for j in jobs if j[0] in idnames]

# 🌈 MASSILLA MAGIC ✨
for s, _ in massilla_powerup_skills:
    freqskills[s] = 30000  # WARNING: ARBRITRARY LARGE VALUE

# TOPs
print("TOP 20 less demanded skills")
print(sorted(freqskills.items(), key=lambda k: k[1])[:20])
print("TOP 20 more demanded skills")
print(sorted(freqskills.items(), key=lambda k: -k[1])[:20])


# skillnames
# skillnames = [s[1] for s in skills]

# import json
# with open('knc_skillnames.json', 'w') as fout:
#     json.dump(skillnames, fout)

# raise ValueError("DEBUG BREAK !!!")

# IDEA:
# ----------
# find the most frequent keyword of a job, and used as Y
#

# TODO: This part slows down

y_keywords = [max((freqskills[js], js) for js in jss)[1] for jss in jobskills]
print("y_keywords[:20] = ↓↓↓")
print(y_keywords[:20])

x_keywords = [None] * len(jobskills)
for i in range(len(jobs)):
    x_keywords[i] = [s in jobskills[i] for s in skillnames]
    # x_keywords[i] = [(s in jobskills[i] and s != y_keywords[i]) for s in skillnames]

print("x_keywords[:20][:10] = ↓↓↓")
for xk in x_keywords[:20]:
    print(xk[:10])


# IA 🌈✨ ######################################################

# Splitting data into training and testing data
print("train_test_split")
X_train, X_test, y_train, y_test = train_test_split(
    x_keywords,
    y_keywords,
    test_size = 0.3,
    random_state = 100
)

print("Time to do fancy calculations")

knc = KNeighborsClassifier(
    n_neighbors=KNC_GROUPS, # The number of neighbours to consider
    weights='uniform',      # How to weight distances
    algorithm='auto',       # Algorithm to compute the neighbours
    leaf_size=30,           # The leaf size to speed up searches
    p=2,                    # The power parameter for the Minkowski metric
    metric='minkowski',     # The type of distance to use
    metric_params=None,     # Keyword arguments for the metric function
    n_jobs=8,               # How many parallel jobs to run
)

print("FREEING MEMORY")
del x_keywords, y_keywords

print("Fitting the model")
knc.fit(X_train, y_train)
predictions = knc.predict(X_test)

print("=" * 80)
print("predictions[:20]")
print(predictions[:20])

print("=" * 80)

# def predict(search_skills):
#     # myskills = {"ARDUINO", "PHP", "MYSQL"}
#     myskills = set(search_skills)
#     vec = [(s in myskills) for s in skillnames]
#     result = knc.predict([vec])
#     return [name for s, name in massilla_powerup_skills if s in result]

# print(predict(["ARDUINO", "PHP", "MYSQL"]))

print("=" * 80)
print("  ACCURACY SCORE =", accuracy_score(y_test, predictions))
print("=" * 80)

print("Saving IA to ia/knc.pkl")
with open('ai/knc.pkl', 'wb') as f:
    pickle.dump(knc, f)

################################################################
