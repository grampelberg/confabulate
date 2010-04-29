#
# Copyright(c) 2010, Thomas Rampelberg <thomas@saunter.org>
# All rights reserved.
#

__date__ = "%date%"
__version__ = "%version%"

from xml.etree import cElementTree as ElementTree

tag_name = lambda x: x.tag.rsplit('}', 1)[-1]

def xml_to_dict(xml):

    # This is a hack to maintain whether a tag is always a list or not.
    list_elements = [ 'Message', 'QueueUrl' ]

    def collapse(a, b):
        # There are a lot of edge cases to this, but hopefully it'll work.
        name = tag_name(b)
        edict = elem_to_dict(b)
        if name in a:
            a[name].append(edict)
        elif name in list_elements:
            a[name] = [edict]
        else:
            a[name] = edict
        return a

    def elem_to_dict(elem):
        name = tag_name(elem)
        children = elem.getchildren()
        if children:
            return reduce(collapse, children, {})
        else:
            return elem.text
    return elem_to_dict(ElementTree.XML(xml))
