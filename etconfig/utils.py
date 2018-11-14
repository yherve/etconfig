# -*- coding: utf-8 -*-
"""
various xml transformation functions
"""
from __future__ import print_function, unicode_literals
from copy import deepcopy

def el_to_struct(elt, print_root=True):
    children = []

    attrs = dict(elt.attrib)
    # if len(attrs):
    #     children.append(attrs)
    # else:
    #     children.append({})

    if elt.text:
        attrs["_TEXT"] = elt.text

    children.append(attrs)

    for ch in elt:
        ch_struct = el_to_struct(ch)
        children.append(ch_struct)

    if len(children) == 1 and children[0] is None:
        children={}

    if print_root:
        res = {elt.tag:children}
    else:
        res = children[1:]
    return res


def elt_merge(change, base):
    """
    merge 'change' element into 'base'

    :param change: instance of Element
    :param base: instance of Element

    :returns: nothing, 'base' object changed directly
    """
    for k,v in change.attrib.items():
        base.set(k, v)
    for child_change in change:
        child_base = base.find(child_change.tag)
        if child_base is not None:
            elt_merge(child_change, child_base)
        else:
            # adding new node. just need to deep copy
            base.append(deepcopy(child_change))
