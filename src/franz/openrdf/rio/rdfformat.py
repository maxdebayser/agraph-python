################################################################################
# Copyright (c) 2006-2017 Franz Inc.  
# All rights reserved. This program and the accompanying materials are
# made available under the terms of the MIT License which accompanies
# this distribution, and is available at http://opensource.org/licenses/MIT
################################################################################

from __future__ import unicode_literals
from builtins import object
import os


class RDFFormat(object):
    """
    Represents the concept of an RDF data serialization format. RDF formats are
    identified by a {@link #getName() name} and can have one or more associated
    MIME types, zero or more associated file extensions and can specify a
    default character encoding. Some formats are able to encode context
    information while others are not; this is indicated by the value of
    supports_contexts field. Similaraly, formats for which the
    supports_attributes flag is True are capable of encoding triple attributes.
    """
    # A global dictionary mapping extensions to formats
    ext_map = {}

    @staticmethod
    def register(fmt):
        """ Register a format object."""
        for ext in fmt.file_extensions:
            RDFFormat.ext_map['.' + ext.lower()] = fmt

    @staticmethod
    def rdf_format_for_file_name(filename):
        """ 
        Try to guess appropriate RDF format from a file name.
        Return a pair (format, compression) where format is
        an RDF format or None (if no matching format was found)
        and compression is a supported compression method
        (currently either None or "gzip").
        """
        compression = None
        root, ext = os.path.splitext(filename)
        if ext.lower() == ".gz":
            compression = "gzip"
            _, ext = os.path.splitext(root)
        fmt = RDFFormat.ext_map.get(ext.lower())
        return fmt, compression
            
    def __init__(self, name, mime_types=None, charset="UTF-8",
                 file_extensions=None, supports_namespaces=False,
                 supports_contexts=False, supports_attributes=False,
                 register=True):
        """
        Initialize a new RDF format object.

        :param name: Human-readable name of the format.
        :param mime_types: A list of MIME types used for this format.
                           The first element of this list will be used
                           as the content-type header during uploads.
        :param charset: Character set used by the format.
        :param file_extensions: List of file extensions for this format.
        :param supports_namespaces: If true, the format supports namespaces
                                    and qualified names. This has no impact
                                    on the Python API.
        :param supports_contexts: If True the format can store quads
                                  (and not just triples).
        :param supports_attributes: If True the format can represent triple
                                    attributes.
        :param register: If True file extensions will be added to the map
                         used by :func:`RDFFormat.rdf_format_for_file_name`.
        """
        self.name = name
        self.mime_types = mime_types
        self.charset = charset
        self.file_extensions = file_extensions
        self.supports_namespaces = supports_namespaces
        self.supports_contexts = supports_contexts
        self.supports_attributes = supports_attributes
        if register:
            RDFFormat.register(self)

    # A call to create_default_formats at the end of this file
    # will convert these dicts to RDFFormat instances.

    RDFXML = dict(
        name="RDF/XML",
        mime_types=["application/rdf+xml", "application/xml"],
        file_extensions=["rdf", "rdfs", "owl", "xml"],
        supports_namespaces=True, supports_contexts=False)

    NTRIPLES = dict(
        name="N-Triples",
        mime_types=["application/n-triples", "text/plain"],
        file_extensions=["nt", "ntriples"],
        supports_namespaces=False, supports_contexts=False)

    NQUADS = dict(
        name="N-Quads",
        mime_types=["application/n-quads"],
        file_extensions=["nq", "nquads"],
        supports_namespaces=False, supports_contexts=True)

    NQX = dict(
        name="Extended N-Quads (with attributes)",
        mime_types=["application/x-extended-nquads"],
        file_extensions=["nqx"],
        supports_namespaces=False, supports_contexts=True,
        supports_attributes=True)

    TURTLE = dict(
        name="Turtle",
        mime_types=["text/turtle"],
        file_extensions=["ttl", "turtle"],
        supports_namespaces=True,
        supports_contexts=False)

    TRIG = dict(
        name="TriG",
        mime_types=["application/trig"],
        file_extensions=["trig"],
        supports_namespaces=True,
        supports_contexts=True)

    TRIX = dict(
        name="TriX",
        mime_types=["application/trix"],
        file_extensions=["trix"],
        supports_namespaces=True,
        supports_contexts=True)


# Convert static dicts inside RDFFormat to instances
def create_default_formats():
    for name in vars(RDFFormat):
        value = getattr(RDFFormat, name)
        if name.isupper() and isinstance(value, dict):
            setattr(RDFFormat, name, RDFFormat(**value))

create_default_formats()
