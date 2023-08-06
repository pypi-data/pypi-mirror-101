from collections import defaultdict
from pathlib import Path
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union

from progress.bar import Bar
from pydantic import BaseModel
from pyimporters_plugins.base import KnowledgeParserBase, Term, KnowledgeParserOptions
from pyimporters_skos.skos import SKOSOptions, SKOSOptionsModel
from rdflib import Graph, RDF, SKOS, URIRef
from rdflib.resource import Resource


class SKOSRFKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar : Bar) -> Generator[Term, None, None]:
        options = SKOSOptions(**options) if isinstance(options, dict) else options
        bar.max = 20
        bar.start()
        g = Graph()
        thes = g.parse(source=str(source), format=options.rdf_format)
        bar.next(20)
        bar.max = len(list(thes.subjects(predicate=RDF.type, object=SKOS.Concept)))
        for curi in thes[:RDF.type:SKOS.Concept]:
            bar.next()
            c = Resource(g, curi)
            status = uri2value(c, "https://www.luaplab.com/resource/srm/2.0/terminology#status")
            workStatus = uri2value(c, "https://www.luaplab.com/resource/srm/2.0/terminology#workStatus")
            variants = list(
                c.objects(URIRef("https://www.luaplab.com/resource/srm/2.0/terminology#syntacticVariantAllowed")))
            variants.extend(
                c.objects(URIRef("https://www.luaplab.com/resource/srm/2.0/terminology#abbreviationAllowed")))
            variants.extend(
                c.objects(URIRef("https://www.luaplab.com/resource/srm/2.0/terminology#acronymAllowed")))

            concept: Term = None
            for prefLabel in c.objects(SKOS.prefLabel):
                if prefLabel.language.startswith(options.lang):
                    concept: Term = Term(identifier=str(curi), preferredForm=prefLabel.value)
            for altLabel in c.objects(SKOS.altLabel):
                if altLabel.language.startswith(options.lang):
                    variants.append(altLabel.value)
            if concept:
                if variants:
                    concept.properties = { "altForms" : [v.value for v in variants] }
                yield concept
        bar.finish()

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return SKOSOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SKOSOptionsModel

def uri2value(concept, uri):
    val = None
    vals = list(concept.objects(URIRef(uri)))
    if vals:
        qname = vals[0].qname()
        toks = qname.split(":")
        if len(toks) == 2:
            val = toks[1]
    return val