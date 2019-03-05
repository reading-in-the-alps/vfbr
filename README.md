# Verfachbuchregister-App

A [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject) based web application to publish summaries of Verfachbücher from

* Stadtgericht Bruneck
* Landgericht St. Michaelsburg
* a third one to come

for the years 1750-1800 created by Michael Prokosch and Michael Span in the context of the FWF-funded project Reading in the Alps.


## enrich workflow

### extract Persons

* annotate 'Person' using generose annotation rules.
* train a model 'data/extract_persons'
* use this model to create NerSamples
* iterate over NerSamples (providing 'generose Person objects') and store Person objects (don't use get or create but a person object for each detected entitiy).
* in theory each Person entity should be linked to the according VfbEntry, but this is not the case. The reason is in this lines
```
    ner, _ = NerSample.objects.get_or_create(text=y[0])
    ...
    ner.content_object = x
```
So better skip the step of creating NerSamples.

# reduce dublicates

compare each Person.written_name wich each other and check the similarity
```python
import itertools
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
persons = Person.objects.all()
for a, b in itertools.combinations(persons, 2):
    score = similar(a.written_name, b.written_name)
    if score > 0.7 and score < 1:
        print(score, a, b)
```

### create trainingsdata by annotating NerSamples

### use trainingsdata to train a model

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
