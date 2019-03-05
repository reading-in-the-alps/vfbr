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
