# Verfachbuchregister-App

A [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject) based web application to publish summaries of Verfachbücher from

* Stadtgericht Bruneck
* Landgericht St. Michaelsburg
* a third one to come

for the years 1750-1800 created by Michael Prokosch and Michael Span in the context of the FWF-funded project Reading in the Alps.


## enrich workflow


### create trainingsdata by annotating NerSamples
*  http://127.0.0.1:8000/annotations/nersamples/todo
* dump checked samples `python manage.py dump_checked_samples`

### use trainingsdata to train a model
* copy dumped samples to `spacyapp/data` e.g. `spacyapp/data/vfbr_jobs.csv`
* configure `spacyapp/train.py`

```python
def main(
    model=None,
    output_dir="data/vfbr_jobs_blank_560_100",
    n_iter=100,
    train_data="data/vfbr_jobs.csv",
    n_samples=560,
    new_label="OBJECT"
):
```

### use this model to create new NerSamples

* change code in spacyapp to use latest model
* start spacyapp `python manage.py runserver 7000`
* start a jupyter notebook session and execute:

```python
from annotations.utils import create_ner_sample_from_qs

NerSample.objects.all().delete() # delete existing NerSamples

spacyurl = "http://127.0.0.1:7000/query/nerparser-api/"

for x in create_ner_sample_from_qs(
    'entities', 'person', 'written_name', spacyurl
):
    pass
```
### repeat the steps above until the model performs good enough

* When checking NerSamples you should try to work on samples which weren't part of the previous trainings material.

### create 'final' NerSamples

* This time you don't need to split your corrected samples into train and test set.

### extract the annotated information form the lates NerSamples and store them.

* This step depends on the actual data/task. E.g. for the jobs dataset, Persons could be explicitly linked to SkosConcepts via a ManyToMany field called 'profession'. This was done with something like:

```python
for x in NerSample.objects.exclude():
    rel_obj = x.content_object
    for y in x.return_ents():
        job, _ = SkosConcept.objects.get_or_create(
                pref_label=y
            )
        job.collection.add(prof_coll)
        rel_obj.profession.add(job)
```
