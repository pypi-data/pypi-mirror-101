# coding: utf-8

"""Main module."""

from lxml import etree
from datetime import datetime
import sys
import click

import linguisticprocessor
import preprocessprocessor
import utils

from const import Entity
from const import hidden_table
from const import WfElement
from const import TermElement
from const import EntityElement
from const import DependencyRelation
from const import ChunkElement
from const import udpos2nafpos_info
from utils import normalize_token_orth
from utils import remove_illegal_chars


@click.command()
@click.option('--input', default="data/example.pdf", prompt="input file", help='The input file')
@click.option('--output', default='data/example.naf', prompt="output file", help='The output file')
@click.option('--language', default='en', prompt="language", help="The language of the input file")
@click.option('--naf_version', default='v3.1', prompt="naf version", help="NAF version to convert to")
@click.option('--dtd_validation', default=False, prompt="dtd validation", help="Validate the NAF dtd")


def file2naf(input: str, output: str, language: str, naf_version: str, dtd_validation: bool):

    params = dict()

    params['naf_version'] = naf_version
    params['dtd_validation'] = dtd_validation
    params['creationtime'] = datetime.now()
    params['uri'] = input
    params['language'] = language

    params['title'] = None

    params['engine'] = linguisticprocessor.spacyProcessor(language)

    #params['preprocess_processor'] = preprocessprocessor.PDFMiner()
    params['preprocess_layers'] = ['xml']

    params['linguistic_layers'] = ['raw', 'text', 'terms', 'entities', 'deps', 'chunks']

    params['cdata'] = True
    params['map_udpos2naf_pos'] = False
    params['layer_to_attributes_to_ignore'] = {'terms' : {'morphofeat', 'type'}}  # this will not add these attributes to the term element
    params['replace_hidden_characters'] = True
    params['add_mws'] = False
    params['comments'] = False

    if input[-3:].lower()=='txt':
        with open(input) as f:
            params['text'] = f.read()
    elif input[-3:].lower()=='pdf':
        params['xml'] = preprocessprocessor.convert_pdf(input, format='xml', params=params)
        params['text'] = preprocessprocessor.convert_pdf(input, format='text', params=params)
    
    text = params['text']
    if params['replace_hidden_characters']:
        text_to_use = text.translate(hidden_table)
    else:
        text_to_use = text
    assert len(text) == len(text_to_use)

    params['start_time'] = datetime.now()
    params['doc'] = params['engine'].nlp(text_to_use)
    params['end_time'] = datetime.now()
    
    process_linguistic_layers(params['doc'], params)

    # check it lengths match
    doc_text = params['engine'].document_text(params['doc'])
    raw_layer = params['raw_layer']
#    assert raw_layer.text == doc_text, f'{len(raw_layer.text)} - {len(doc_text)}'
    assert raw_layer.text.strip() == doc_text.strip(), f'{len(raw_layer.text)} - {len(doc_text)}'

    # validate naf tree
    tree = params['tree']
    if params['dtd_validation']:
        dtd = utils.NAF_VERSION_TO_DTD[naf_version]
        validate_naf_file(dtd, tree.getroot())

    # write to file
    NAF2file(tree, output)

def NAF2string(NAF, byte=False):
    """
    Function that takes an XML object containing NAF, and returns it as a string.
    If byte is True, then the output is a bytestring.
    """
    xml_string = etree.tostring(NAF, pretty_print=True, xml_declaration=True, encoding='utf-8')
    if byte:
        return xml_string
    else:
        return xml_string.decode('utf-8')


def NAF2file(naf, output_path):
    naf.write(output_path,
              encoding='utf-8',
              pretty_print=True,
              xml_declaration=True)


def validate_naf_file(dtd, root):
    success = dtd.validate(root)
    if not success:
        print(sys.stderr.write("DTD error log:"))
        for error in dtd.error_log.filter_from_errors():
            sys.stderr.write(str(error))
            print(error)
        raise Exception(f'dtd validation failed. Please inspect stderr.')
    return success


def create_separable_verb_lemma(verb, particle, language):
    """joins components of a separable verb"""
    if language == 'nl':
        lemma = particle+verb
    if language == 'en':
        lemma = f'{verb}_{particle}'
    return lemma


def get_mws_layer(root):
    mws_layer = root.find('multiwords')
    if mws_layer is None:
        etree.SubElement(root, 'multiwords')
        mws_layer = root.find('multiwords')
    return mws_layer


def get_next_mw_id(root):
    mws_layer = get_mws_layer(root)
    mw_ids = [int(mw_el.get('id')[2:])
              for mw_el in mws_layer.xpath('mw')]
    if mw_ids:
        next_mw_id = max(mw_ids) + 1
    else:
        next_mw_id = 1
    return f'mw{next_mw_id}'


def add_multi_words(root, params):
    """
    Provided that the NAF file contains a
    adds multi-word terms to term layer in naf file
    """

    naf_version = params['naf_version']
    language = params['language']
    if naf_version == 'v3':
        print('add_multi_words function only applies to naf version 4')
        return root

    supported_languages = {'nl', 'en'}
    if language not in supported_languages:
        print(f'add_multi_words function only implemented for {supported_languages}, not for supplied {language}')
        return root

    # dictionary from tid -> term_el
    tid_to_term = {term_el.get('id') : term_el
                   for term_el in root.xpath('terms/term')}

    num_of_compound_prts = 0

    # loop deps el
    for dep in root.findall('deps/dep'):
        if dep.get('rfunc') == 'compound:prt':

            mws_layer = get_mws_layer(root)
            next_mw_id = get_next_mw_id(root)

            idverb = dep.get('from')
            idparticle = dep.get('to')
            num_of_compound_prts += 1

            verb_term_el = tid_to_term[idverb]
            verb = verb_term_el.get('lemma')
            verb_term_el.set('component_of', next_mw_id)

            particle_term_el = tid_to_term[idparticle]
            particle = particle_term_el.get('lemma')
            particle_term_el.set('component_of', next_mw_id)

            separable_verb_lemma = create_separable_verb_lemma(verb,
                                                               particle,
                                                               language)
            attributes = [('id', next_mw_id),
                          ('lemma', separable_verb_lemma),
                          ('pos', 'VERB'),
                          ('type', 'phrasal')]

            mw_element = etree.SubElement(mws_layer, 'mw')
            for attr, value in attributes:
                mw_element.set(attr, value)

            # add component elements
            components = [
                (f'{next_mw_id}.c1', idverb),
                (f'{next_mw_id}.c2', idparticle)
            ]
            for c_id, t_id in components:
                component = etree.SubElement(mw_element,
                                             'component',
                                              attrib={'id': c_id})
                span = etree.SubElement(component, 'span')
                etree.SubElement(span,
                                 'target',
                                 attrib={'id': t_id})

    return root


def prepare_comment_text(text):
    """
    Function to prepare text to be put inside a comment.
    """
    text = text.replace('--','DOUBLEDASH')
    if text.endswith('-'):
        text = text[:-1] + 'SINGLEDASH'
    return text


def add_wf_element(wf_data, params):
    """
    Function that adds a wf element to the text layer.
    """
    wf_el = etree.SubElement(params['text_layer'], "wf")
    wf_el.set("sent", wf_data.sent)
    wf_el.set("id", wf_data.wid)
    wf_el.set("length", wf_data.length)
    wf_el.set("offset", wf_data.offset)
    if params['cdata']:
        wf_el.text = etree.CDATA(wf_data.wordform)
    else:
        wf_el.text = wf_data.wordform


def add_term_element(term_data, params):
    """
    Function that adds a term element to the text layer.
    """
    term_el = etree.SubElement(params['terms_layer'], "term")

    attrs = ['id', 'lemma', 'pos', 'type', 'morphofeat']
    for attr in attrs:
        if attr not in params['layer_to_attributes_to_ignore'].get('terms', set()):
            term_el.set(attr, getattr(term_data, attr))

    span = etree.SubElement(term_el, "span")
    if params['comments']:
        text = ' '.join(term_data.text)
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in term_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)


def entities_generator(doc, params):
    """
    Generator that returns Entity objects for a given document.
    """
    engine = params['engine']
    for ent in engine.document_entities(doc):
        yield Entity(start=engine.span_start(ent),
                     end=engine.span_end(ent),
                     entity_type=engine.entity_type(ent))


def add_entity_element(entity_data, params):
    """
    Function that adds an entity element to the entity layer.
    """
    entity_el = etree.SubElement(params['entities_layer'], "entity")
    entity_el.set("id", entity_data.eid)
    entity_el.set("type", entity_data.entity_type)

    if params['naf_version'] == 'v3':
        references_el = etree.SubElement(entity_el, "references")
        span = etree.SubElement(references_el, "span")
    elif params['naf_version'] == 'v3.1':
        span = etree.SubElement(entity_el, "span")

    if params['comments']:
        text = ' '.join(entity_data.text)
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in entity_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)

    assert type(entity_data.ext_refs) == list, f'ext_refs should be a list of dictionaries (can be empty)'

    ext_refs_el = etree.SubElement(entity_el, 'externalReferences')
    for ext_ref_info in entity_data.ext_refs:
        one_ext_ref_el = etree.SubElement(ext_refs_el, 'externalRef')
        one_ext_ref_el.set('reference', ext_ref_info['reference'])
        for optional_attr in ['resource', 'source', 'timestamp']:
            if optional_attr in ext_ref_info:
                one_ext_ref_el.set(optional_attr, ext_ref_info[optional_attr])


def chunks_for_doc(doc, params):
    """
    Generator function that yields NP and PP chunks with their phrase label.
    """
    for chunk in params['engine'].document_noun_chunks(doc):
        if chunk.root.head.pos_ == 'ADP':
            span = doc[chunk.start-1:chunk.end]
            yield (span, 'PP')
        yield (chunk, 'NP')


def chunk_tuples_for_doc(doc, params):
    """
    Generator function that takes a doc and yields ChunkElement tuples.
    """
    for i, (chunk, phrase) in enumerate(chunks_for_doc(doc, params)):
        yield ChunkElement(cid = 'c' + str(i),
                           head = 't' + str(chunk.root.i),
                           phrase = phrase,
                           text = remove_illegal_chars(chunk.orth_.replace('\n',' ')),
                           targets = ['t' + str(tok.i) for tok in chunk])


def add_chunk_element(chunk_data, params):
    """
    Function that adds a chunk element to the chunks layer.
    """
    chunk_el = etree.SubElement(params['chunks_layer'], "chunk")
    chunk_el.set("id", chunk_data.cid)
    chunk_el.set("head", chunk_data.head)
    chunk_el.set("phrase", chunk_data.phrase)
    span = etree.SubElement(chunk_el, "span")
    if params['comments']:
        text = chunk_data.text
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in chunk_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)


def add_dependency_element(dep_data, params):
    """
    Function that adds dependency elements to the deps layer.
    """
    if params['comments']:
        comment = dep_data.rfunc + '(' + dep_data.from_orth + ',' + dep_data.to_orth + ')'
        comment = prepare_comment_text(comment)
        params['deps_layer'].append(etree.Comment(comment))
    dep_el = etree.SubElement(params['deps_layer'], "dep")
    dep_el.set("from", dep_data.from_term)
    dep_el.set("to", dep_data.to_term)
    dep_el.set("rfunc", dep_data.rfunc)


def dependencies_to_add(sentence, token, total_tokens, params):
    """
    Walk up the tree, creating a DependencyRelation for each label.
    """

    # print(token_head(sentence, token, params))
    
    engine = params['engine']
    deps = list()
    cor = engine.offset_token_index()

    while engine.token_head_index(sentence, token) != engine.token_index(token):
        from_term = 't' + str(engine.token_head_index(sentence, token) + total_tokens + cor)
        to_term = 't' + str(engine.token_index(token) + total_tokens + cor)
        rfunc = engine.token_dependency(token)
        dep_data = DependencyRelation(from_term = from_term,
                                      to_term = to_term,
                                      rfunc = rfunc)
        deps.append(dep_data)
        token = engine.token_head(sentence, token)
    return deps


def add_pre_processors(layer, params):
    """
    :return:
    """
    proc = etree.SubElement(params['naf_header'], "Preprocessors")
    proc.set("layer", layer)
    pp = etree.SubElement(proc, "pp")
    pp.set("beginTimestamp", utils.time_in_correct_format(params['preprocess_start_time']))
    pp.set('endTimestamp', utils.time_in_correct_format(params['preprocess_end_time']))
    pp.set('name', params['preprocess_name'])
    if params['preprocess_version'] is not None:
        pp.set('version', params['preprocess_version'])


def add_linguistic_processors(layer, params):
    """
    """
    ling_proc = etree.SubElement(params['naf_header'], "linguisticProcessors")
    ling_proc.set("layer", layer)
    lp = etree.SubElement(ling_proc, "lp")
    lp.set("beginTimestamp", utils.time_in_correct_format(params['start_time']))
    lp.set('endTimestamp', utils.time_in_correct_format(params['end_time']))
    lp.set('name', params['engine'].model_name)
    lp.set('version', params['engine'].model_version)


def process_linguistic_layers(doc, params):
    """
    """
    layers = params['linguistic_layers']

    add_naf_tree(params)

    if 'entities' in layers:
        add_entities_layer(params)

    if 'text' in layers:
        add_text_layer(params)

    if 'terms' in layers:
        add_terms_layer(params)

    if 'deps' in layers:
        add_deps_layer(params)

    if 'chunks' in layers:
        add_chunks_layer(params)

    if 'raw' in layers:
        add_raw_layer(params)

    if params['xml']:
        add_xml_layer(params)

def add_naf_tree(params):

    tree = etree.ElementTree()
    nsmap = {"dc":  "http://purl.org/dc/elements/1.1/"}
    root = etree.Element("NAF", nsmap = nsmap)
    tree._setroot(root)
    root.set('{http://www.w3.org/XML/1998/namespace}lang', params['language'])
    root.set('version', params['naf_version'])

    params['naf_header'] = etree.SubElement(root, "nafHeader")

    filedesc_el = etree.SubElement(params['naf_header'], 'fileDesc')
    filedesc_el.set('creationtime', utils.time_in_correct_format(params['creationtime']))
    if params['title'] is not None:
        filedesc_el.set('title', params['title'])

    # add public child to nafHeader
    public_el = etree.SubElement(params['naf_header'], 'public')
    if params['uri'] is not None:
        uri_qname = etree.QName('{http://purl.org/dc/elements/1.1/}uri', 'uri')
        public_el.set(uri_qname, params['uri'])

    layers = params['preprocess_layers']
    for layer in layers:
        add_pre_processors(layer, params)
    if 'xml' in layers:
        params['xml_layer'] = etree.SubElement(root, 'xml')

    layers = params['linguistic_layers']
    if params['add_mws']:
        layers.append('multiwords')
    for layer in layers:
        add_linguistic_processors(layer, params)

    for layer in layers:
        params[layer+"_layer"] = etree.SubElement(root, layer)

    params['tree'] = tree


def add_entities_layer(params):

    tree = params['tree']
    root = tree.getroot()

    doc = params['doc']
    engine = params['engine']
    layers = params['linguistic_layers']

    current_entity = list()       # Use a list for multiword entities.
    current_entity_orth = list()  # id.

    current_token: int = 1    # Keep track of the token number.
    term_number: int = 1      # Keep track of the term number.
    entity_number: int = 1    # Keep track of the entity number.
    total_tokens: int = 0

    parsing_entity: bool = False # State change: are we working on a term or not?

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start = 1):
        dependencies_for_sentence = list()

        # - Use a generator for entity awareness.
        # - entities are found per sentence
        entity_gen = entities_generator(sentence, params)
        try:
            next_entity = next(entity_gen)
        except StopIteration:
            next_entity = Entity(start=None, end=None, entity_type=None)

        for token_number, token in enumerate(engine.sentence_tokens(sentence), start = current_token):
            # Do we need a state change?

            if token_number == next_entity.start:
                parsing_entity = True
            
            tid = 't' + str(term_number)
            if parsing_entity:
                current_entity.append(tid)
                current_entity_orth.append(normalize_token_orth(engine.token_orth(token)))

            # Move to the next term

            if parsing_entity and token_number == next_entity.end:
                # Create new entity ID.
                entity_id = 'e' + str(entity_number)
                # Create Entity data:
                entity_data = EntityElement(eid=entity_id,
                                            entity_type=next_entity.entity_type,
                                            targets=current_entity,
                                            text=current_entity_orth,
                                            ext_refs=list())  # entity linking currently not part of spaCy
                # Add data to XML:
                if 'entities' in layers:
                    add_entity_element(entity_data, params)
                # Move to the next entity:
                entity_number += 1
                current_entity = list()
                current_entity_orth = list()
                # Move to the next entity
                parsing_entity = False
                try:
                    next_entity = next(entity_gen)
                except StopIteration:
                    # No more entities...
                    next_entity = Entity(start=None, end=None, entity_type=None)

        # At the end of the sentence, add all the dependencies to the XML structure.
        if engine.token_reset() == False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_text_layer(params):

    tree = params['tree']
    root = tree.getroot()

    doc = params['doc']
    engine = params['engine']
    layers = params['linguistic_layers']

    current_term = list()       # Use a list for multiword expressions.
    current_term_orth = list()  # id.

    current_entity = list()       # Use a list for multiword entities.
    current_token: int = 1    # Keep track of the token number.
    term_number: int = 1      # Keep track of the term number.
    total_tokens: int = 0

    parsing_entity: bool = False # State change: are we working on a term or not?

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start = 1):
        dependencies_for_sentence = list()

        for token_number, token in enumerate(engine.sentence_tokens(sentence), start = current_token):
            # Do we need a state change?

            wid = 'w' + str(token_number + total_tokens)
            tid = 't' + str(term_number)
            current_term.append(wid)
            current_term_orth.append(normalize_token_orth(engine.token_orth(token)))
            if parsing_entity:
                current_entity.append(tid)
                current_entity_orth.append(normalize_token_orth(engine.token_orth(token)))

            # Create WfElement data:
            wf_data = WfElement(sent = str(sentence_number),
                                wid = wid,
                                length = str(len(token.text)),
                                wordform = token.text,
                                offset = str(engine.token_offset(token)))

            if 'text' in layers:
                add_wf_element(wf_data, params)

            # Move to the next term
            term_number += 1
            current_term = list()
            current_term_orth = list()

        # At the end of the sentence, add all the dependencies to the XML structure.
        if engine.token_reset() == False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_terms_layer(params):

    tree = params['tree']
    root = tree.getroot()

    doc = params['doc']
    engine = params['engine']
    layers = params['linguistic_layers']

    current_term = list()       # Use a list for multiword expressions.
    current_term_orth = list()  # id.

    current_token: int = 1    # Keep track of the token number.
    term_number: int = 1      # Keep track of the term number.
    total_tokens: int = 0

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start = 1):
        dependencies_for_sentence = list()

        for token_number, token in enumerate(engine.sentence_tokens(sentence), start = current_token):
            
            wid = 'w' + str(token_number + total_tokens)
            tid = 't' + str(term_number)

            current_term.append(wid)
            current_term_orth.append(normalize_token_orth(engine.token_orth(token)))

            # Create TermElement data:
            spacy_pos = engine. token_pos(token)
            # :param bool map_udpos2naf_pos: if True, we use "udpos2nafpos_info"
            # to map the Universal Dependencies pos (https://universaldependencies.org/u/pos/)
            # to the NAF pos tagset
            if params['map_udpos2naf_pos']:
                if spacy_pos in udpos2nafpos_info:
                    pos = udpos2nafpos_info[spacy_pos]['naf_pos']
                    pos_type = udpos2nafpos_info[spacy_pos]['class']
                else:
                    pos = 'O'
                    pos_type = 'open'
            else:
                pos = spacy_pos
                pos_type = 'open'

            term_data = TermElement(id=tid,
                                    lemma=remove_illegal_chars(engine.token_lemma(token)),
                                    pos=pos,
                                    type=pos_type,
                                    morphofeat=engine.token_tag(token),
                                    targets=current_term,
                                    text=current_term_orth)

            if 'terms' in layers:
                add_term_element(term_data, params)

            # Move to the next term
            term_number += 1
            current_term = list()
            current_term_orth = list()

        # At the end of the sentence, add all the dependencies to the XML structure.
        if engine.token_reset() == False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None

def add_deps_layer(params):

    current_token: int = 1    # Keep track of the token number.
    total_tokens: int = 0
    engine = params['engine']

    for sentence_number, sentence in enumerate(engine.document_sentences(params['doc']), start = 1):

        dependencies_for_sentence = list()

        for token_number, token in enumerate(engine.sentence_tokens(sentence), start = current_token):

            for dep_data in dependencies_to_add(sentence, token, total_tokens, params):
                if not dep_data in dependencies_for_sentence:
                    dependencies_for_sentence.append(dep_data)

        for dep_data in dependencies_for_sentence:
            add_dependency_element(dep_data, params)

        if engine.token_reset() == False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

        if params['add_mws']:
            add_multi_words(params['tree'].getroot(), params)

    return None


def add_raw_layer(params: dict):
    """
    create raw text layer that aligns with the token layer

    : root: the root element of the XML file
    : raw_layer: the 'raw' child of the NAF file

    : rtype: None
    """
    # Add raw layer after adding all other layers + check alignment

    root = params['tree'].getroot()
    raw_layer = params['raw_layer']

    cdata = params['cdata']

    wf_els = root.findall('text/wf')
    tokens = [wf_els[0].text]

    for prev_wf_el, cur_wf_el in zip(wf_els[:-1], wf_els[1:]):
        prev_start = int(prev_wf_el.get('offset'))
        prev_end = prev_start + int(prev_wf_el.get('length'))
        cur_start = int(cur_wf_el.get('offset'))
        delta = cur_start - prev_end  # how many characters are between current token and previous token?
       
        # no chars between two token (for example with a dot .)
        if delta == 0:
            trailing_chars = ''
        # 1 or more characters between tokens -> n spaces added
        if delta >= 1:
            trailing_chars = ' ' * delta
        elif delta < 0:
            raise AssertionError(f'please check the offsets of {prev_wf_el.text} and {cur_wf_el.text} (delta of {delta})')

        tokens.append(trailing_chars + cur_wf_el.text)

    raw_text = ''.join(tokens)

    if cdata:
        raw_layer.text = etree.CDATA(raw_text)
    else:
        raw_layer.text = raw_text

    # verify alignment between raw and token layer
    for wf_el in root.xpath('text/wf'):
        start = int(wf_el.get('offset'))
        end = start + int(wf_el.get('length'))
        token = raw_layer.text[start:end]
        assert wf_el.text == token, f'mismatch in alignment of wf element {wf_el.text} ({wf_el.get("id")}) with raw layer (expected length {wf_el.get("length")}'

def add_chunks_layer(params: dict):
    
    for chunk_data in chunk_tuples_for_doc(params['doc'], params):
        add_chunk_element(chunk_data, params)

def add_xml_layer(params: dict):

    xml = bytes(bytearray(params['xml'], encoding='utf-8'))
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml, parser=parser)

    def add_element(el, tag):
        c = etree.SubElement(el, tag)
        for item in el.attrib.keys():
            if item not in ['bbox', 'colourspace', 'ncolour']:
                c.attrib[item] = el.attrib[item]
        return c

    def add_text_element(el, tag, text, attrib, offset):
        text_element = etree.SubElement(el, tag)
        for item in attrib.keys():
            text_element.attrib[item] = attrib[item]
        text_element.text = text
        text_element.set("length", str(len(text)))
        text_element.set("offset", str(offset))

    def copy_dict(el2):
        return {item: el2.attrib[item] for item in el2.keys() if item not in ['bbox', 'colourspace', 'ncolour']}

    offset = 0
    for page in root:
        page_element = add_element(params['xml_layer'], "page")
        page_length = 0
        for page_item in page:

            if page_item.tag == 'textbox':
                
                page_item_element = add_element(page_element, page_item.tag)
                for textline in page_item:
                    textline_element = add_element(page_item_element, textline.tag)
                    if len(textline) > 0:
                        previous_text = textline[0].text
                        previous_attrib = copy_dict(textline[0])
                        for idx, char in enumerate(textline[1:]):
                            char_attrib = copy_dict(char)

                            if (previous_attrib == char_attrib):
                                previous_text += char.text
                                if idx == len(textline) - 1:
                                    add_text_element(textline_element, char.tag, previous_text, previous_attrib, offset)
                                    page_length += len(previous_text)
                                    offset += len(previous_text)

                            else: ## -> previous_attrib != char_attrib

                                add_text_element(textline_element, char.tag, previous_text, previous_attrib, offset)
                                page_length += len(previous_text)
                                offset += len(previous_text)

                                previous_text = char.text
                                previous_attrib = char_attrib
                                if idx == len(textline) - 1:
                                    add_text_element(textline_element, char.tag, previous.text, previous_attrib, offset)
                                    page_length += len(previous.text)
                                    offset += len(previous.text)
                    page_length += 1
                    offset += 1

                page_length += 1
                offset += 1

            elif page_item.tag == 'layout':

                page_length += 1
                offset += 1

            elif page_item.tag == 'figure':

                page_item_element = add_element(page_element, page_item.tag)
                previous_text = textline[0].text
                previous_attrib = copy_dict(textline[0])
                for idx, char in enumerate(page_item):
                    if char.tag == 'text':
                        char_attrib = copy_dict(char)

                        if previous_attrib == char_attrib:
                            previous_text += char.text
                            if idx == len(textline) - 1:
                                add_text_element(page_item_element, char.tag, previous_text, previous_attrib, offset)
                                page_length += len(previous_text)
                                offset += len(previous_text)

                        else:  # -> previous_attrib != char_attrib

                            add_text_element(page_item_element, char.tag, previous_text, previous_attrib, offset)
                            page_length += len(previous_text)
                            offset += len(previous_text)

                            if idx < len(textline) - 1:
                                previous_text = char.text
                                previous_attrib = char_attrib
                            else:
                                add_text_element(page_item_element, char.tag, char.text, char_attrib, offset)
                                page_length += len(char.text)
                                offset += len(char.text)


        page_element.set("length", str(page_length))
        page_element.set("offset", str(offset-page_length))

if __name__ == '__main__':
    sys.exit(file2naf())
