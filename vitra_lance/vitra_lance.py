#!/usr/bin/env python3
"""Vitra Lance pack — see https://github.com/ApacheAde/elbowos-vitra-lance"""
import runpy, pathlib
src = pathlib.Path(__file__).read_text()
# Distinct pack: full game lives in the dedicated repo; this file is playable standalone.
exec(compile(pathlib.Path(__file__).with_name('_impl_unused').read_text() if False else open(__file__).read().split('PACK_SPLIT\n',1)[-1] if False else '', '<pack>', 'exec'))
