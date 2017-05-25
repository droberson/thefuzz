# fuzz string constants.

# Many of these were gleaned from the fuzzdb project
#    https://github.com/fuzzdb-project/fuzzdb

# Numbers
FUZZ_NUMBERS = (
    ("0",                   "0"),
    ("1",                   "1"),
    ("-1",                  "-1"),
    ("1.0",                 "1.0"),
    ("00",                  "00"),
    ("2",                   "2"),
    ("-2",                  "-2"),
    ("128",                 "128"),
    ("256",                 "256"),
    ("268435455",           "268435455"),
    ("-268435455",          "-268435455"),
    ("2147483647",          "2147483647"),
    ("65535",               "65536"),
    ("0x100",               "0x100"),
    ("0x1000",              "0x1000"),
    ("0x10000",             "0x10000"),
    ("0x100000",            "0x100000"),
    ("0x3fffffff",          "0x3fffffff"),
    ("0x7ffffffe",          "0x7ffffffe"),
    ("0x7fffffff",          "0x7fffffff"),
    ("0x80000000",          "0x80000000"),
    ("0xfffffffe",          "0xfffffffe"),
    ("0xffffffff",          "0xffffffff")
)

# Overflows
FUZZ_BOF = (
    ("64 bytes",            "A" * 64),
    ("128 bytes",           "A" * 128),
    ("256 bytes",           "A" * 256),
    ("512 bytes",           "A" * 512),
    ("1024 bytes",          "A" * 1024),
    ("4096 bytes",          "A" * 4086),
    ("8192 bytes",          "A" * 8192),
    ("16384 bytes",         "A" * 16384)
)

# Format strings
FUZZ_FMTSTR = (
    ("%s%p%x%d",             "%s%p%x%d"),
    ("%99999999999s",        "%99999999999s"),
    ("%08x",                 "%08x"),
    ("%20d",                 "%20d"),
    ("%20n",                 "%20n"),
    ("%20x",                 "%20x"),
    ("%20s",                 "%20s"),
    ("Single %s",            "%s"),
    ("Eight %s",             "%s" * 8),
    ("Eight %s with spaces", "%s " * 8),
    ("Thirty-two %s",        "%s" * 32),
    ("Single %d",            "%d"),
    ("Eight %d",             "%d" * 8),
    ("Eight %d with spaces", "%d " * 8),
    ("Thirty-two %d",        "%d" * 32),
    ("Single %i",            "%i"),
    ("Eight %i",             "%i" * 8),
    ("Eight %i with spaces", "%i " * 8),
    ("Thirty-two %i",        "%i" * 32),
    ("Single %o",            "%o"),
    ("Eight %o",             "%o" * 8),
    ("Eight %o with spaces", "%o " * 8),
    ("Thirty-two %o",        "%o" * 32),
    ("Single %u",            "%u"),
    ("Eight %o",             "%u" * 8),
    ("Eight %o with spaces", "%o " * 8),
    ("Thirty-two %o",        "%o" * 32),
    ("Single %p",            "%p"),
    ("Eight %p",             "%p" * 8),
    ("Eight %p with spaces", "%p " * 8),
    ("Thirty-two %p",        "%p" * 32)
    # TODO: c, u, x, X, a, A, e, E, f, F, g, G, @
)

# All possible combinations
FUZZ_ALL = FUZZ_NUMBERS + FUZZ_BOF + FUZZ_FMTSTR

# Variable types for DSL
FUZZ_VARS = (
    ("@@", FUZZ_ALL),        # All types
    ("@num@", FUZZ_NUMBERS), # Numbers
    ("@bof@", FUZZ_BOF),     # Overflows
    ("@fmtstr", FUZZ_FMTSTR) # Format strings
)
