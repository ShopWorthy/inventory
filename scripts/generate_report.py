#!/usr/bin/env python3
"""Stub report generation script called by the export endpoint."""
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--format', default='csv')
args = parser.parse_args()

# Stub: write placeholder content
with open(args.output, 'w') as f:
    f.write(f"# ShopWorthy Inventory Report\n")
    f.write(f"# Format: {args.format}\n")
    f.write("product_id,product_name,stock_count\n")

print(f"Report written to {args.output}")
