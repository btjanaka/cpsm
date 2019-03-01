# Configuration file for CPSM

# User info
username = "btjanaka"
fullname = "Bryon Tjanaka"

# Command to run on the files when starting a new solution
editor = "vim -p"

# Abbreviations for directories and full names of websites/contests/etc
abbreviations = {
    "uva": {
        "name": "UVa",
        "dir": "uva",
    },
    "kattis": {
        "name": "Kattis",
        "dir": "kattis",
    },
    "hr": {
        "name": "Hackerrank",
        "dir": "hackerrank"
    },
    "lc": {
        "name": "LeetCode",
        "dir": "leetcode",
    },
}

# Mapping of languages to templates
templates = {
    "cpp":
    """\
// Author: $USERNAME ($FULLNAME)
// Problem: ($NAME) $PROBLEM_NAME
#include <bits/stdc++.h>
#define GET(x) scanf("%d", &x)
#define GED(x) scanf("%lf", &x)
typedef long long ll;
using namespace std;
typedef pair<int, int> ii;

int main() {

  return 0;
}
""",
    "py":
    """\
# Author: $USERNAME ($FULLNAME)
# Problem: ($NAME) $PROBLEM_NAME

import sys
from collections import defaultdict

""",
}
