"""
StudyChart AI - C++ Engine Python Interface.
"""

import sys
import os
import importlib.util

cpp_engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cpp-engine", "cpp_bridge.py"))
if not os.path.exists(cpp_engine_path):
    cpp_engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cpp-engine", "cpp_bridge.py"))

spec = importlib.util.spec_from_file_location("cpp_bridge", cpp_engine_path)
cpp_bridge_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpp_bridge_module)

cpp_engine = cpp_bridge_module.cpp_engine
test_cpp_engine = cpp_bridge_module.test_cpp_engine
