#!/usr/bin/env python
# -*- coding: utf-8 -*-
# h2m@access.uzh.ch

import os
import sys

from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer

from bioc import BioCAnnotation
from bioc import BioCXMLReader
from bioc import BioCXMLWriter

BIOC_IN = os.path.join('..', 'test_input', 'example_input.xml')
BIOC_OUT = os.path.join('..', 'test_input', 'example_input_stemmed.xml')
DTD_FILE = os.path.join('..', 'test_input', 'BioC.dtd')


def main():
    # Use file defined by BIOC_IN as default if no other provided
    bioc_in = BIOC_IN
    if len(sys.argv) >= 2:
        bioc_in = sys.argv[1]

    # A BioCXMLReader object is put in place to hold the example BioC XML
    # document
    bioc_reader = BioCXMLReader(bioc_in, dtd_valid_file=DTD_FILE)

    # A BioCXMLWRiter object is prepared to write out the annotated data
    bioc_writer = BioCXMLWriter(BIOC_OUT)

    # The NLTK porter stemmer is used for stemming
    stemmer = PorterStemmer()

    # The example input file given above (by BIOC_IN) is fed into
    # a BioCXMLReader object; validation is done by the BioC DTD
    bioc_reader.read()

    # Pass over basic data
    bioc_writer.collection = bioc_reader.collection

    # Get documents to manipulate
    documents = bioc_writer.collection.documents

    # Go through each document
    annotation_id = 0
    for document in documents:

        # Go through each passage of the document
        for passage in document:
            #  Stem all the tokens found
            stems = [stemmer.stem(token) for
                     token in wordpunct_tokenize(passage.text)]
            # Add an anotation showing the stemmed version, in the
            # given order
            for stem in stems:
                annotation_id += 1

                # For each token an annotation is created, providing
                # the surface form of a 'stemmed token'.
                # (The annotations are collectively added following
                #  a document passage with a <text> tag.)
                bioc_annotation = BioCAnnotation()
                bioc_annotation.text = stem
                bioc_annotation.id = str(annotation_id)
                bioc_annotation.put_infon('surface form',
                                          'stemmed token')
                passage.add_annotation(bioc_annotation)

    # Print file to screen w/o trailing newline
    # (Can be redirected into a file, e. g output_bioc.xml)
    sys.stdout.write(str(bioc_writer))

    # Write to disk
    bioc_writer.write()


if __name__ == '__main__':
    main()
