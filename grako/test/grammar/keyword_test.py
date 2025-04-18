# -*- coding: utf-8 -*-
# Copyright (C) 2017      by Juancarlo Añez
# Copyright (C) 2012-2016 by Juancarlo Añez and Thomas Bragg
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

# from grako.exceptions import FailedParse     # TODO - parser-related import, currently unused
# from grako.codegen import codegen            # TODO - parser-related import, currently unused
from grako.tool import compile


class KeywordTests(unittest.TestCase):

    def test_keywords_in_rule_names(self):
        grammar = r'''
            start
                =
                whitespace
                ;

            whitespace
                =
                    {'x'}+
                ;
        '''
        m = compile(grammar, 'Keywords')
        m.parse('x')

    def test_python_keywords_in_rule_names(self):
        # This is a regression test for
        # https://bitbucket.org/neogeny/grako/issues/59
        # (semantic actions not called for rules with the same name as a python
        # keyword).
        grammar = r'''
            not = 'x' ;
        '''
        m = compile(grammar, 'Keywords')

        class Semantics(object):
            def __init__(self):
                self.called = False

            def not_(self, ast):
                self.called = True

        semantics = Semantics()
        m.parse('x', semantics=semantics)
        assert semantics.called

    def test_define_keywords(self):
        pass
        # TODO parser is not used annymore as of Python 3.10, so this test must be removed or completely changed
        # # import parser
        #
        # grammar = r'''
        #     @@keyword :: B C
        #     @@keyword :: 'A'
        #
        #     start = ('a' 'b').{'x'}+ ;
        # '''
        # model = compile(grammar, "test")
        # c = codegen(model)
        # # parser.suite(c)
        #
        # grammar2 = str(model)
        # model2 = compile(grammar2, "test")
        # c2 = codegen(model2)
        # # parser.suite(c2)
        #
        # self.assertEqual(grammar2, str(model2))

    def test_check_keywords(self):
        pass
        # TODO parser is not used annymore as of Python 3.10, so this test must be removed or completely changed
        # # import parser
        #
        # grammar = r'''
        #     @@keyword :: A
        #
        #     start = {id}+ $ ;
        #
        #     @name
        #     id = /\w+/ ;
        # '''
        # model = compile(grammar, 'test')
        # c = codegen(model)
        # parser.suite(c)
        #
        # ast = model.parse('hello world')
        # self.assertEqual(['hello', 'world'], ast)
        #
        # try:
        #     ast = model.parse("hello A world")
        #     self.assertEqual(['hello', 'A', 'world'], ast)
        #     self.fail('accepted keyword as name')
        # except FailedParse as e:
        #     self.assertTrue('"A" is a reserved word' in str(e))
        #     pass

    def test_check_unicode_name(self):
        grammar = r'''
            @@keyword :: A

            start = {id}+ $ ;

            @name
            id = /\w+/ ;
        '''
        model = compile(grammar, 'test')
        model.parse("hello Øresund")
