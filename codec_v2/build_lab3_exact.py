"""Compatibility entry point. Authoritative assignment: PDF page 9, variant 1.
The PDF page 6 example must never be substituted for the assignment.
"""
from build_lab3_variant1_forms import canonical, split_net

def build():return canonical(False)
if __name__=='__main__':print(build())
