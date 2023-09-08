import spacy
import huspacy
import textacy

if not spacy.util.is_package("hu_core_news_lg"):
    huspacy.download("hu_core_news_lg")

nlp = huspacy.load()


########################################################################################################################
#####                                                Common helper functions                                       #####
########################################################################################################################
def _clean_up_text(strng):
    """Remove >>exotic<< characters that confuse NER"""
    bad_chars = "“#$%&'()*+\"-—"
    for bad_char in bad_chars:
        strng = strng.replace(bad_char, " ")
    strng = strng.split()
    strng = [e.strip() for e in strng]
    return " ".join(strng).lower()


def _remove_overlappings(lst):
    """Remove overlapping strings from lst"""
    lst.sort(key=len)
    return sorted([x for i, x in enumerate(lst) if x not in ",".join(lst[i + 1 :])])


def _remove_article(strng):
    """Remove starting article >>a/az/egy<< from strng"""
    if strng.startswith("az "):
        return strng.replace("az ", "")
    elif strng.startswith("a "):
        return strng.replace("a ", "")
    elif strng.startswith("egy "):
        return strng.replace("egy ", "")
    else:
        return strng


def _remove_acronym(lst_of_acronyms, strng):
    for acronym in lst_of_acronyms:
        if strng.startswith(acronym + " "):
            strng = strng.replace(acronym + " ", "")
        if strng.endswith(" " + acronym):
            strng = strng.replace(acronym + " ", "")
    return strng


########################################################################################################################
#####                                            Keyword extractor                                                 #####
########################################################################################################################
def extract_keywords(article):
    article = _clean_up_text(article)
    doc = nlp(article)
    no_keywords = 10

    # extract keywords using various algorithms
    text_rank = textacy.extract.keyterms.textrank(
        doc,
        normalize="lemma",
        include_pos=["NOUN", "PROPN", "ADJ"],
        position_bias=True,
        topn=no_keywords,
    )
    yake = textacy.extract.keyterms.yake(
        doc,
        normalize="lemma",
        ngrams=(2, 3),
        include_pos=["NOUN", "PROPN", "ADJ"],
        window_size=3,
        topn=no_keywords,
    )
    scake = textacy.extract.keyterms.scake(
        doc, normalize="lemma", include_pos=["NOUN", "PROPN", "ADJ"], topn=no_keywords
    )
    sgrank = textacy.extract.keyterms.sgrank(
        doc,
        normalize="lemma",
        ngrams=(1, 2, 3),
        include_pos=["NOUN", "PROPN", "ADJ"],
        window_size=3000,
        topn=no_keywords,
    )

    # acronym finder
    acronyms = textacy.extract.acros.acronyms_and_definitions(doc)

    # clean up keywords
    text_rank = [_remove_acronym(list(acronyms.keys()), e[0]) for e in text_rank]
    yake = [_remove_acronym(list(acronyms.keys()), e[0]) for e in yake]
    scake = [_remove_acronym(list(acronyms.keys()), e[0]) for e in scake]
    sgrank = [_remove_acronym(list(acronyms.keys()), e[0]) for e in sgrank]

    for k in list(acronyms.keys()):  # delete acronyms without definitions
        if not acronyms[k]:
            del acronyms[k]

    # NER extraction
    entities = [str(ent) for ent in doc.ents]
    labels = [ent.label_ for ent in doc.ents]
    # find the list of possible entities with their tags here https://huggingface.co/flair/ner-english-ontonotes-large
    # GPE - geopolitical entity, LOC - location name, ORG - organization
    entity_types = ["GPE", "ORG", "PERSON", "LOC", "PRODUCT"]
    output_tags = set()
    for e in zip(labels, entities):
        if e[0] in entity_types:
            output_tags.add(e[1])
    output_tags = [
        _remove_acronym(list(acronyms.keys()), _remove_article(e)) for e in output_tags
    ]
    output_tags = _remove_overlappings(output_tags)

    output_tags = set(output_tags).union(acronyms.values())
    output_tags = {e for e in output_tags if e not in acronyms.keys()}

    # filter out keywords
    text_rank = _remove_overlappings([e for e in text_rank if e not in output_tags])
    yake = _remove_overlappings([e for e in yake if e not in output_tags])
    scake = _remove_overlappings([e for e in scake if e not in output_tags])
    sgrank = _remove_overlappings([e for e in sgrank if e not in output_tags])
    common_keywords = set.intersection(
        set(text_rank), set(yake), set(scake), set(sgrank)
    )

    output_tags = output_tags.union(common_keywords)

    tag_len = len(output_tags)
    if tag_len < 20:
        i = int((20 - tag_len) / 2)
        text_rank = [e for e in text_rank if e not in output_tags][:i]
        sgrank = [e for e in sgrank if e not in output_tags][:i]
        output_tags = set.union(output_tags, set(text_rank), set(sgrank))

    output_tags = _remove_overlappings(list(output_tags))
    return output_tags
