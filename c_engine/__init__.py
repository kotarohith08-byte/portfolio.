"""
StudyChart AI - C Engine Python Interface.
"""

import sys
import os
import importlib.util

c_engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "c-engine", "c_bridge.py"))
if not os.path.exists(c_engine_path):
    c_engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "c-engine", "c_bridge.py"))

spec = importlib.util.spec_from_file_location("c_bridge", c_engine_path)
c_bridge_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c_bridge_module)

c_engine = c_bridge_module.c_engine
test_c_engine = c_bridge_module.test_c_engine
