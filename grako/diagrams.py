# -*- coding: utf-8 -*-
# Copyright (C) 2017      by Juancarlo Añez
# Copyright (C) 2012-2016 by Juancarlo Añez and Thomas Bragg
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import itertools

from grako.walkers import NodeWalker

try:
    import pygraphviz as pgv
except Exception:
    raise


__all__ = ['draw']


def draw(filename, grammar):
    traverser = GraphvizWalker()
    traverser.walk(grammar)
    traverser.draw(filename)


class GraphvizWalker(NodeWalker):
    def __init__(self):
        super(GraphvizWalker, self).__init__()
        self.top_graph = pgv.AGraph(directed=True,
                                    rankdir='LR',
                                    packMode='clust',
                                    splines='true'
                                    )
        self.stack = [self.top_graph]
        self.node_count = 0

    @property
    def graph(self):
        return self.stack[-1]

    def draw(self, filename):
        self.graph.layout(prog='dot')
        # WARNING: neato generated graphics hang my GPU
        # self.graph.layout(prog='neato')
        self.graph.draw(filename)

    def push_graph(self, name=None, **attr):
        if name is None:
            self.node_count += 1
            name = 'g%d' % self.node_count
        self.stack.append(self.graph.add_subgraph(name, **attr))
        return self.graph

    def pop_graph(self):
        self.stack.pop()
        pass

    def node(self, name, id=None, **attr):
        if id is None:
            self.node_count += 1
            id = 'n%d' % self.node_count
        else:
            try:
                return self.graph.get_node(id)
            except KeyError:
                pass
        self.graph.add_node(id, **attr)
        n = self.graph.get_node(id)
        n.attr['label'] = name
#        n.attr['shape'] = 'circle'
        return n

    def tnode(self, name, **attr):
        return self.node(name, **attr)

    def dot(self):
        n = self.node('')
        n.attr['shape'] = 'point'
        n.attr['size'] = 0.0000000001
        n.attr['label'] = ''
        return n

    def start_node(self):
        return self.dot()

    def ref_node(self, name):
        n = self.node(name)
        n.attr['shape'] = 'box'
        return n

    def rule_node(self, name, **attr):
        n = self.node(name, **attr)
        n.attr['shape'] = 'parallelogram'
        return n

    def end_node(self):
        n = self.node('')
        n.attr['shape'] = 'point'
        n.attr['width'] = 0.1
        return n

    def edge(self, s, e, **attr):
        self.graph.add_edge(s, e, **attr)
        edge = self.graph.get_edge(s, e)
        # edge.attr['arrowhead'] = 'normal'
        edge.attr['arrowhead'] = 'none'
        return edge

    def redge(self, s, e):
        edge = self.edge(s, e)
        edge.attr['dir'] = 'back'
        return edge

    def zedge(self, s, e):
        edge = self.edge(s, e, len=0.000001)
        return edge

    def nedge(self, s, e):
        return self.edge(s, e, style='invisible', dir='none')

    def path(self, p):
        self.graph.add_path(p)

    def subgraph(self, name, bunch):
        self.top_graph.add_subgraph(name)

    def concat(self, *args):
        return list(itertools.chain(*args))

    def _walk_decorator(self, d):
        return self.walk(d.exp)

    def _walk__Decorator(self, d):
        return self._walk_decorator(d)

    def walk_default(self, node):
        raise Exception('No walking for ', type(node).__name__)

    def walk_Grammar(self, g):
        self.push_graph(g.name + '0')
        try:
            vrules = [self.walk(r) for r in reversed(g.rules)]
        finally:
            self.pop_graph()
        self.push_graph(g.name + '1')
        try:
            # link all rule starting nodes with invisible edges
            starts = [self.node(r.name, id=r.name) for r in g.rules]
            for n1, n2 in zip(starts, starts[1:]):
                # self.nedge(n1, n2)
                pass
        finally:
            self.pop_graph()
        s, t = vrules[0][0], vrules[-1][1]
        return (s, t)

    def walk_Rule(self, r):
        self.push_graph(r.name)
        try:
            i, e = self.walk(r.exp)
            s = self.rule_node(r.name, id=r.name)
            self.edge(s, i)
            t = self.end_node()
            self.edge(e, t)
            return (s, t)
        finally:
            self.pop_graph()

    def walk_BasedRule(self, r):
        return self.walk_Rule(r)

    def walk_RuleRef(self, rr):
        n = self.ref_node(rr.name)
        return (n, n)

    def walk_Special(self, s):
        n = self.node(s.special)
        return (n, n)

    def walk_Override(self, o):
        return self._walk_decorator(o)

    def walk_Named(self, n):
        return self._walk_decorator(n)

    def walk_NamedList(self, n):
        return self._walk_decorator(n)

    def walk_Cut(self, c):
        # c = self.node('>>')
        # return (c, c)
        return None

    def walk_Optional(self, o):
        i, e = self._walk_decorator(o)
        ni = self.dot()
        ne = self.dot()
        self.zedge(ni, i)
        self.edge(ni, ne)
        self.zedge(e, ne)
        return (ni, ne)

    def walk_Closure(self, r):
        self.push_graph(rankdir='TB')
        try:
            i, e = self._walk_decorator(r)
            ni = self.dot()
            self.edge(ni, i)
            self.edge(e, ni)
            return (ni, ni)
        finally:
            self.pop_graph()

    def walk_PositiveClosure(self, r):
        i, e = self._walk_decorator(r)
        if i == e:
            self.redge(e, i)
        else:
            self.edge(e, i)
        return (i, e)

    def walk_Join(self, r):
        i, e = self._walk_decorator(r)
        n = self.tnode(r.sep)
        self.edge(i, n)
        self.edge(n, e)
        return (i, e)

    def walk_Group(self, g):
        return self._walk_decorator(g)

    def walk_Choice(self, c):
        vopt = [self.walk(o) for o in c.options]
        vopt = [o for o in vopt if o is not None]
        ni = self.dot()
        ne = self.dot()
        for i, e in vopt:
            self.edge(ni, i)
            self.edge(e, ne)
        return (ni, ne)

    def walk_Sequence(self, s):
        vseq = [self.walk(x) for x in s.sequence]
        vseq = [x for x in vseq if x is not None]
        i, _ = vseq[0]
        _, e = vseq[-1]
        if i != e:
            bunch = zip([a for _x, a in vseq[:-1]],
                        [b for b, _y in vseq[1:]])
            for n, n1 in bunch:
                self.edge(n, n1)
        return (i, e)

    def walk_Lookahead(self, looky):
        i, e = self._walk_decorator(looky)
        n = self.node('&')
        self.edge(n, e)
        return (n, e)

    def walk_NegativeLookahead(self, looky):
        i, e = self._walk_decorator(looky)
        n = self.node('!')
        self.edge(n, e)
        return (n, e)

    def walk_RuleInclude(self, looky):
        i, e = self._walk_decorator(looky)
        n = self.node('>')
        self.edge(n, e)
        return (n, e)

    def walk_Pattern(self, p):
        n = self.tnode(p.pattern)
        return (n, n)

    def walk_Token(self, t):
        n = self.tnode(t.token)
        return (n, n)

    def walk_Void(self, v):
        n = self.dot()
        return (n, n)

    def walk_Constant(self, t):
        n = self.tnode('`%s`' % t.ast)
        return (n, n)

    def walk_EOF(self, v):
        # n = self.node('$')
        # return (n, n)
        return None
