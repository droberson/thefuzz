# fuzz string constants.
# Many of these were gleaned from the fuzzdb project
#    https://github.com/fuzzdb-project/fuzzdb

# Numbers
FUZZ_NUMBERS = (
    ("Zero",                "0"),
    ("One",                 "1"),
    ("Negative 1",          "-1")
)

# Overflows
FUZZ_BOF = (
    ("128 bytes",           "A" * 128),
    ("256 bytes",           "A" * 256),
    ("512 bytes",           "A" * 512),
    ("1024 bytes",          "A" * 1024),
    ("4096 bytes",          "A" * 4086),
    ("8192 bytes",          "A" * 8192)
)

# Format strings
FUZZ_FMTSTR = (
    ("%s%p%x%d",             "%s%p%x%d"),
    ("%99999999999s",        "%99999999999s"),
    ("Single %s",            "%s"),
    ("Eight %s",             "%s" * 8),
    ("Eight %s with spaces", "%s " * 8),
    ("Thirty-two %s",        "%s" * 32),
    ("Single %d",            "%d"),
    ("Eight %d",             "%d" * 8),
    ("Eight %d with spaces", "%d " * 8),
    ("Thirty-two %d",        "%d" * 32)
    # TODO: i, o, u, x, X, a, A, e, E, f, F, g, G, p, @
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
