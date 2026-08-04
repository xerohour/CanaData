#!/bin/bash
echo "Running system scalability audit benchmarks..."
PYTHONPATH=.:./parse-script pytest performance_tests/test_system_scalability_audit.py --benchmark-json=audit_benchmark.json -v
