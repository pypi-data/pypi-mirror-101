#!/usr/bin/env python3

import sys
from line_profiler import LineProfiler
import radical.analytics as ra

sid = sys.argv[1]

def main():
    ra.Session(sid, "radical.pilot")

if __name__ == "__main__":
    main()

