#!/usr/bin/python3.3
# -*- coding: utf-8 -*-
#
# Patches that should be applied to modules/packages code just before
# being embedded in the executable/archive at runtime

import ast

def patch_matplotlib(mod):
    tree = ast.parse(mod.__source__)

    class ChangeDef(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if node.name == '_get_data_path':
                node.body = ast.parse('return os.path.join(os.path.dirname(sys.executable), "mpl-data")').body
            return node

    t = ChangeDef()
    patched_tree = t.visit(tree)

    mod.__code_object__ = compile(patched_tree, mod.__file__, "exec", optimize=mod.__optimize__)
