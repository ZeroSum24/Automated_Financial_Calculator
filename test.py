

strn = "EUHWC - Expense Claims (Responses)"
strn_t = "EUHWC - Refund Claims (Responses)"
print(strn)

def replace(string: str):

    string = string.replace(" ", "_")
    return string

strn = replace(strn)
strn_t = replace(strn_t)

print("Replaced: {0}".format(strn))
print("Replaced: {0}".format(strn_t))

def string_man(string: str):

    base = string.split("_-_")[1]
    base = base.split("_(")[0]
    base = base.split("_")[0]

    base = "{0}s".format(base)

    return base.lower()

print(string_man(strn))
print(string_man(strn_t))

# strn = workbook.replace('%2F', '_')
#
# strn
# print(strn)
