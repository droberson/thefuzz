"""
fuzz string constants.

Many of these were gleaned from the fuzzdb project and the big list of naughty
strings. Their respective project pages are here:

    https://github.com/fuzzdb-project/fuzzdb
    https://github.com/minimaxir/big-list-of-naughty-strings
"""

# These are formatted as follows:
# ("description", "actual string")
#
# "description" id displayed on output, "actual string" is sent during fuzzing

import string

# Numbers
FUZZ_NUMBERS = [
    ("0", "0"),
    ("1", "1"),
    ("-1", "-1"),
    ("1.0", "1.0"),
    ("00", "00"),
    ("2", "2"),
    ("-2", "-2"),
    ("128", "128"),
    ("256", "256"),
    ("-2147483648", "-2147483648"),
    ("268435455", "268435455"),
    ("-268435455", "-268435455"),
    ("2147483647", "2147483647"),
    ("65535", "65536"),
    ("0x100", "0x100"),
    ("0x1000", "0x1000"),
    ("0x10000", "0x10000"),
    ("0x100000", "0x100000"),
    ("0x3fffffff", "0x3fffffff"),
    ("0x7ffffffe", "0x7ffffffe"),
    ("0x7fffffff", "0x7fffffff"),
    ("0x80000000", "0x80000000"),
    ("0xfffffffe", "0xfffffffe"),
    ("0xffffffff", "0xffffffff")
]

# Reserved strings
FUZZ_RESERVED = [
    ("hasOwnProperty", "hasOwnProperty"),
    ("true", "true"),
    ("True", "True"),
    ("TRUE", "TRUE"),
    ("false", "false"),
    ("False", "False"),
    ("FALSE", "FALSE"),
    ("null", "null"),
    ("NULL", "NULL"),
    ("(null)", "(null"),
    ("nil", "nil"),
    ("NIL", "NIL"),
    ("None", "None"),
    ("undefined", "undefined"),
    ("undef", "undef"),
    ("\\", "\\"),
    ("\\\\", "\\\\")
]

# Overflows
FUZZ_BOF = [
    ("64 bytes", "A" * 64),
    ("128 bytes", "A" * 128),
    ("256 bytes", "A" * 256),
    ("512 bytes", "A" * 512),
    ("1024 bytes", "A" * 1024),
    ("4096 bytes", "A" * 4086),
    ("8192 bytes", "A" * 8192),
    ("16384 bytes", "A" * 16384)
]

# Format strings
FUZZ_FMTSTR = [
    ("%s%p%x%d", "%s%p%x%d"),
    ("%99999999999s", "%99999999999s"),
    ("%08x", "%08x"),
    ("%20d", "%20d"),
    ("%20n", "%20n"),
    ("%20x", "%20x"),
    ("%20s", "%20s"),
    ("Single %x", "%x"),
    ("Eight %x", "%x" * 8),
    ("Eight %x with spaces", "%x " * 8),
    ("Thirty-two %x", "%x" * 32),
    ("Single %s", "%s"),
    ("Eight %s", "%s" * 8),
    ("Eight %s with spaces", "%s " * 8),
    ("Thirty-two %s", "%s" * 32),
    ("Single %d", "%d"),
    ("Eight %d", "%d" * 8),
    ("Eight %d with spaces", "%d " * 8),
    ("Thirty-two %d", "%d" * 32),
    ("Single %i", "%i"),
    ("Eight %i", "%i" * 8),
    ("Eight %i with spaces", "%i " * 8),
    ("Thirty-two %i", "%i" * 32),
    ("Single %o", "%o"),
    ("Eight %o", "%o" * 8),
    ("Eight %o with spaces", "%o " * 8),
    ("Thirty-two %o", "%o" * 32),
    ("Single %u", "%u"),
    ("Eight %o", "%u" * 8),
    ("Eight %o with spaces", "%o " * 8),
    ("Thirty-two %o", "%o" * 32),
    ("Single %p", "%p"),
    ("Eight %p", "%p" * 8),
    ("Eight %p with spaces", "%p " * 8),
    ("Thirty-two %p", "%p" * 32),
    ("Single %c", "%c"),
    ("Eight %c", "%c" * 8),
    ("Eight %c with spaces", "%c " * 8),
    ("Thirty-two %c", "%c" * 32),
    ("Single %u", "%u"),
    ("Eight %u", "%u" * 8),
    ("Eight %u with spaces", "%u " * 8),
    ("Thirty-two %u", "%u" * 32),
    ("Single %X", "%X"),
    ("Eight %X", "%X" * 8),
    ("Eight %X with spaces", "%X " * 8),
    ("Thirty-two %X", "%X" * 32),
    ("Single %a", "%a"),
    ("Eight %a", "%a" * 8),
    ("Eight %a with spaces", "%a " * 8),
    ("Thirty-two %a", "%a" * 32),
    ("Single %A", "%A"),
    ("Eight %A", "%A" * 8),
    ("Eight %A with spaces", "%A " * 8),
    ("Thirty-two %A", "%A" * 32),
    ("Single %e", "%e"),
    ("Eight %e", "%e" * 8),
    ("Eight %e with spaces", "%e " * 8),
    ("Thirty-two %e", "%e" * 32),
    ("Single %E", "%E"),
    ("Eight %E", "%E" * 8),
    ("Eight %E with spaces", "%E " * 8),
    ("Thirty-two %E", "%E" * 32),
    ("Single %f", "%f"),
    ("Eight %f", "%f" * 8),
    ("Eight %f with spaces", "%f " * 8),
    ("Thirty-two %f", "%f" * 32),
    ("Single %F", "%F"),
    ("Eight %F", "%F" * 8),
    ("Eight %F with spaces", "%F " * 8),
    ("Thirty-two %F", "%F" * 32),
    ("Single %g", "%g"),
    ("Eight %g", "%g" * 8),
    ("Eight %g with spaces", "%g " * 8),
    ("Thirty-two %g", "%g" * 32),
    ("Single %G", "%G"),
    ("Eight %G", "%G" * 8),
    ("Eight %G with spaces", "%G " * 8),
    ("Thirty-two %G", "%G" * 32),
    ("Single %@", "%@"),
    ("Eight %@", "%@" * 8),
    ("Eight %@ with spaces", "%@ " * 8),
    ("Thirty-two %@", "%@" * 32)
]

# Alphanumeric combinations
FUZZ_ALPHANUMERIC = [
    ("a-z", string.ascii_lowercase),
    ("A-Z", string.ascii_uppercase),
    ("a-zA-Z", string.ascii_letters),
    ("0-9", string.digits),
    ("hexadecimal digits", string.hexdigits),
    ("octal digits", string.octdigits),
    ("punctuation", string.punctuation),
    ("printale characters", string.printable),
    ("whitespace", string.whitespace)
]

# Add single characters to FUZZ_ALPHANUMERIC.
for x in string.printable:
    FUZZ_ALPHANUMERIC.insert(0, (x, x))

# All possible combinations
FUZZ_ALL = FUZZ_ALPHANUMERIC + FUZZ_RESERVED + FUZZ_NUMBERS + FUZZ_BOF + FUZZ_FMTSTR

# Variable types for DSL
FUZZ_VARS = (
    ("@@", FUZZ_ALL),                  # All types
    ("@num@", FUZZ_NUMBERS),           # Numbers
    ("@bof@", FUZZ_BOF),               # Overflows
    ("@fmtstr@", FUZZ_FMTSTR),         # Format strings
    ("@reserved@", FUZZ_RESERVED),     # Reserved strings
    ("@alphanum@", FUZZ_ALPHANUMERIC), # Alphanumerics
)
