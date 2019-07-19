import re

def begins_with_constant(string):
    pattern = "(^[^AaEeIiOoUuYy0-9])"
    compiled = re.compile(pattern)
    try:
        result = compiled.match(string)[0]
        return True
    except TypeError:
        return False

def constant_append_to_end(string):
    first_char = string[0]
    string = list(string)
    chopString = string[1:]
    chopString += first_char + 'ay'
    result = "".join(chopString)
    return result.upper()

def vowel_append_to_end(string):
    stringList = list(string)
    stringList += 'ay'
    stringAppended = "".join(stringList)
    return stringAppended.upper()

def evaluate(string):
    if begins_with_constant(string):
        result = constant_append_to_end(string)
        return result
    else:
        result = vowel_append_to_end(string)
        return result

#AWS/FLASK/RDS/CRUD practice - API that returns pig latin translation of the input
#Data is written to RDS tables in AWS
#Elliott Arnold  7-19-19
#si3mshady


#http://initd.org/psycopg/docs/usage.html
#https://pynative.com/python-postgresql-insert-update-delete-table-data-to-perform-crud-operations/
