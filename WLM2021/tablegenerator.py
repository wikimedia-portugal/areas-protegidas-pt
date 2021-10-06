#!/usr/bin/env python3
"""
Copyright (C) 2021 alchimista alchimistawp@gmail.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


def convert(q):
    conversion = {"Q207199": "Lisboa",
                  "Q210527": "Aveiro",
                  "Q244521": "Faro",
                  "Q273525": "Viseu",
                  "Q244512": "Leiria",
                  "Q326203": "Braga",
                  "Q225189": "Portalegre",
                  "Q326214": "Viana do Castelo",
                  "Q379372": "Vila Real",
                  "Q274109": "Setúbal",
                  "Q373528": "Bragança",
                  "Q322792": "Porto",
                  "Q273533": "Guarda",
                  "Q273529": "Castelo Branco",
                  "Q244517": "Coimbra",
                  "Q244510": "Santarém",
                  "Q274118": "Évora",
                  "Q321455": "Beja",
                  "Q10267300": "Distrito de Lamego",
                  "Q10267318": "Distrito do Funchal",
                  "Q4348932": "Distrito de Ponta Delgada",
                  "Q10267294": "Distrito de Angra do Heroísmo",
                  "Q4412409": "Distrito da Horta"}
    return conversion[q]


distritos = "Q207199", "Q210527", "Q225189", "Q244510", "Q244512", "Q244517", "Q244521", "Q273525", "Q273529", "Q273533", "Q274109", "Q274118", "Q321455", "Q322792", "Q326203", "Q326214", "Q373528", "Q379372", "Q4348932", "Q4412409", "Q10267294", "Q10267300", "Q10267318"
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import re

endpoint_url = "https://query.wikidata.org/sparql"


def main(distrito):
    endpoint_url = "https://query.wikidata.org/sparql"
    query1 = '''SELECT DISTINCT ?item ?itemLabel ?idwlm ?localLabel ?municipioLabel ?fonte ?cat ?cats ?button ?coord (GROUP_CONCAT(DISTINCT ?tipoLabel ;separator=", ") AS ?tipos)
    (GROUP_CONCAT(DISTINCT ?classLabel ;separator=", ") AS ?classes)
    WITH {
      SELECT DISTINCT ?item ?local ?municipio ?coord WHERE {
        { ?item wdt:P131 ?local.
         ?local wdt:P131 ?municipio.
         ?municipio wdt:P131 wd:Q210527. } # itens ao nível de freguesia
        UNION
        { ?item wdt:P131 ?local.
         ?local wdt:P131 wd:Q210527.
    BIND(?local AS ?municipio ) } # itens ao nível de concelho
        UNION
        { ?item wdt:P131 wd:'''
    query2 = '''. } # itens ao nível da região

      }
    } as %results
    WHERE {
      INCLUDE %results
      { ?item wdt:P2186 ?idwlm.
        ?item wdt:P625 ?coord.}  # IDWLM

      OPTIONAL { ?item wdt:P31 ?tipo. FILTER ( ?tipo != wd:Q210272)} # Tipo
      OPTIONAL { ?item wdt:P1435 ?class. } # Classificação
      OPTIONAL { ?item wdt:P1702 ?id1. } # ID DGPC
      OPTIONAL { ?item wdt:P1700 ?id2. } # ID SIPA
      {BIND (CONCAT('<a href="http://www.patrimoniocultural.gov.pt/pt/patrimonio/patrimonio-imovel/pesquisa-do-patrimonio/classificado-ou-em-vias-de-classificacao/geral/view/', ?id1, '"', '>DGPC</a>') as ?url1)}
      {BIND (CONCAT('<a href="http://www.monumentos.gov.pt/Site/APP_PagesUser/SIPA.aspx?id=', ?id2, '"', '>SIPA</a>') as ?url2)}
      {BIND (CONCAT(COALESCE( ?url1,''), COALESCE( CONCAT(IF (BOUND (?url1),'<br/>',''), ?url2),'')) AS ?fonte)}
      OPTIONAL {?item wdt:P373 ?cat.}
      {BIND (CONCAT('Images from Wiki Loves Monuments 2021 in Portugal - Aveiro',IF(BOUND(?cat),CONCAT('{{!}}',?cat),'')) AS ?cats)}
    BIND(SUBSTR(STR(?item), 32 ) AS ?id)
      OPTIONAL { ?item schema:description ?descr.
      FILTER((LANG(?descr)) = 'pt') }
      {BIND (CONCAT("https://commons.wikimedia.org/wiki/special:uploadWizard?campaign=wlm-pt&amp;id=", ?id, "&amp;descriptionlang=pt&amp;description=", ENCODE_FOR_URI (?itemLabel), ENCODE_FOR_URI (IF(BOUND(?descr),CONCAT(" - ",?descr),"")), "&amp;categories=", ENCODE_FOR_URI (?cats)) AS ?button)}

      SERVICE wikibase:label { bd:serviceParam wikibase:language 'pt,pt-br,en'.
                             ?class rdfs:label ?classLabel.
                             ?tipo rdfs:label ?tipoLabel.
                             ?item rdfs:label ?itemLabel.
                             ?local rdfs:label ?localLabel.
                             ?municipio rdfs:label ?municipioLabel.
    }
    }
    GROUP BY ?item ?itemLabel ?idwlm ?localLabel ?municipioLabel ?id1 ?fonte ?cat ?cats ?button ?coord
    ORDER BY ?municipioLabel ?localLabel ?itemLabel '''

    _hmtl = '''<tr>
                <td><a href="https://pt.wikipedia.org/wiki/{nome}">
                    {nome}</a></td>
                <td><abbr title="{tipo}">MN</abbr></td>
                <td><a href="https://pt.wikipedia.org/wiki/{municipio}">
                    {municipio}</a></td>
                <td><a title="Item no Wikidata: {wd}" href="https://www.wikidata.org/wiki/{wd}"></a></td>
                <td><a title="Localização no mapa" href="https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lon}&amp;zoom=13"></a></td>
                <td><a href="{button}"></a></td>
                <td>
                    {fontes}
                </td>
            </tr>'''

    tables = '''<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width" />
        <title>WLM PT 2021: Aveiro</title>
        <link rel="stylesheet" href="wlm-tables.css" />
    </head>
    <body>
        <table>
            <tr>
                <th>Nome</th>
                <th>Classificação</th>
                <th>Município</th>
                <th>Wikidata</th>
                <th>Mapa</th>
                <th>Carrega as tuas fotos!</th>
                <th>Fonte</th>
            </tr>'''

    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    query = query1 + distrito + query2
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:

        if result['item']['value'] not in (
                "http://www.wikidata.org/entity/Q49330753", "http://www.wikidata.org/entity/Q9617529"):
            print(result)

            nome = result['itemLabel']['value']
            tipo = result['tipos']['value']
            wd = result['item']['value'].split("/entity/")[1]
            coord = result['coord']['value']
            button = result['button']['value']
            fonte = result['fonte']['value']
            try:
                municipio = result['municipioLabel']['value']
            except:
                municipio = "indefinido"

            button = button.replace(r"%7B%7B%21%7D%7D", "|")
            print(nome, tipo, wd, coord, button, fonte, municipio)
            _coord = coord.split("(")[1].split(")"[0])

            s = re.findall("""\((-?\d+\.\d+)\s(-?\d+\.\d+)\)""", coord)

            lat = s[0][1]
            lon = s[0][0]

            monumento = _hmtl.format(nome=nome, tipo=tipo, municipio=municipio, wd=wd, lat=lat, lon=lon, button=button,
                                     fontes=fonte)

            tables = tables + monumento

    print("\n\n\n\::::\n")
    tables = tables + '''    </table>
    </body>
    </html>'''
    print(tables)

    import os.path
    f_name = os.path.join("pages","wlm-2021-"+convert(distrito) + ".xhtml")
    with open(f_name, 'w') as f:
        f.writelines(tables)


for i in distritos:
    main(i)

