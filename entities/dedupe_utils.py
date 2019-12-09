import pandas as pd

from django.core.exceptions import ObjectDoesNotExist

file = "dedupe/output.csv"

df = pd.read_csv(file)

for item, row in df.iterrows():
    cl_id = row['Cluster ID']
    ent_id = row['ID']
    try:
        per = Person.objects.get(id=ent_id)
    except ObjectDoesNotExist:
        print("oje")
        continue
    per.dedupe_cluster_id = int(cl_id)
    per.save()
