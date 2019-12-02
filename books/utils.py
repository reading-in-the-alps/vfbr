import json
import urllib.request
from urllib.error import HTTPError
from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON


def sanitize_querystring(querystring, startstr):
    san_query = querystring.format(startstr).replace('<**', '{').replace('**>', '}')
    return san_query


query_bsb = """
PREFIX  dc:<http://purl.org/dc/elements/1.1/>
PREFIX  dct:<http://purl.org/dc/terms/>
PREFIX  rdagr1:<http://rdvocab.info/Elements/>
PREFIX  umbel: <http://umbel.org/umbel#>

SELECT * WHERE <**
  ?s umbel:isLike <http://nbn-resolving.de/{}> .
  ?s dct:issued ?when .
  ?s rdagr1:placeOfPublication ?where .
  ?s dct:publisher ?publisher .
  ?s dct:language ?lang .
**>
"""


def get_results(query, endpoint=settings.BSB_ENDPOINT):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result


def lobid_to_data(gnd_id):
    if gnd_id is not None:
        try:
            with urllib.request.urlopen(gnd_id) as url:
                data = json.loads(url.read().decode())
        except HTTPError:
            data = None
            print("ERROR: {}".format(gnd_id))
        return data
    else:
        return None
