# Verfachbuchregister-App

A [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject) based web application to publish summaries of Verfachbücher from

* Stadtgericht Bruneck
* Oberamtsgericht Bruneck
* Landgericht St. Michaelsburg

for the years 1750-1800 created by Michael Prokosch and Michael Span in the context of the FWF-funded project Reading in the Alps.


# enrich workflow

## train custom word vectors

`python -m prodigy terms.train-vectors vfbr_vecs "http://127.0.0.1:8000/api/vfb-entry/?format=json::vollregest::10" --loader from_drf --lang de`

### adm_types

`python -m prodigy ner.make-gold vfbr vfbr_adm_model http://127.0.0.1:8000/api/vfb-entry/?format=json::vollregest::10 --loader from_drf --label ADM-TYPE -U`

### vfbr_pers

`python -m prodigy ner.make-gold vfbr_persons vfbr_vecs "http://127.0.0.1:8000/api/vfb-entry/?format=json::vollregest::10" --loader from_drf --label PERS -U`

`python -m prodigy ner.make-gold vfbr_persons vfbr_vecs "http://127.0.0.1:8000/api/vfb-entry/?format=json::vollregest::10" --loader from_drf --label PERS -U`

### vfbr_place

`python -m prodigy ner.make-gold vfbr_places vfbr_vecs "http://127.0.0.1:8000/api/persons/?format=json::legacy_id::10" --loader from_drf --label PLACE -U`

`python -m prodigy ner.make-gold vfbr_places vfbr_places_model "http://127.0.0.1:8000/api/persons/?format=json::legacy_id::10" --loader from_drf --label PLACE -U`


### vfbr_jobs

`prodigy dataset vfbr_jobs`

`python -m prodigy ner.make-gold vfbr_jobs vfbr_vecs "http://127.0.0.1:8000/api/persons/?format=json::legacy_id::10" --loader from_drf --label JOB -U`

`python -m prodigy ner.make-gold vfbr_jobs vfbr_jobs_model "http://127.0.0.1:8000/api/persons/?format=json::legacy_id::10" --loader from_drf --label JOB -U`

`python -m prodigy ner.batch-train vfbr_jobs vfbr_vecs --output vfbr_jobs_model -U --no-missing`


# teach NN / VN

`prodigy ner.make-gold vfbr_nn vfbr_persons_vecs "http://127.0.0.1:8000/api/persons/?format=json::written_name::10" --loader from_drf --label NN -U`

`prodigy ner.make-gold vfbr_nn vfbr_persons_vecs "http://127.0.0.1:8000/api/persons/?format=json&name=Zwischenpruggerin::written_name::10" --loader from_drf --label NN -U`

`prodigy ner.make-gold vfbr_nn vfbr_persons_vecs "http://127.0.0.1:8000/api/persons/?format=json&ordering=name::written_name::10" --loader from_drf --label NN -U`


`prodigy ner.batch-train vfbr_nn vfbr_persons_vecs --output vfbr_nn_model -U --no-missing`

# teach VN
`prodigy ner.make-gold vfbr_nn vfbr_vn_model "http://127.0.0.1:8000/api/persons/?format=json::written_name::10" --loader from_drf --label VN -U`


## teach terms

`python -m prodigy terms.teach drf vfrb_vecs --seeds seeds.txt `

useless?

## train

`python -m prodigy ner.batch-train vfbr_persons vfbr_vecs --output vfbr_persons_model -U --no-missing`

`python -m prodigy ner.batch-train vfbr_places vfbr_vecs --output vfbr_places_model -U --no-missing`


## teach

`python -m prodigy ner.teach vfbr_quick vfbr_adm_model http://127.0.0.1:8000/api/vfb-entry/?format=json::vollregest::10 --loader from_drf  -U`


## dedupe
```cmd

pip install csvdedupe

mkdir dedupe

cd dedupe

wget -O data.csv  "http://127.0.0.1:8000/entities/person/?columns=forename&columns=name&name=&forename=&written_name=&gender=m%C3%A4nnlich&Filter=Search&_export=csv"

csvdedupe data.csv  --field_names "Umfassende Namensansetzung" Vorname Name --output_file output.csv
```
