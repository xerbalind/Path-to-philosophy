#!/usr/bin/env python3
import json
import cgi
from path import Path

# Lees data verstuurd door JavaScript
parameters = cgi.FieldStorage()

begin = parameters.getvalue("start")
end = parameters.getvalue("end")
language = parameters.getvalue("language")

path = Path(begin, end, language)
path.construct_path()

if path.status_message != "success":
    # Als er een error bericht aanwezig is betekent het dat er iets is mis gelopen
    body = {"error": path}
else:
    body = {"path": path.path}

# Stuur antwoord terug
print("Content-Type: application/json")
print()  # Lege lijn na headers
print(json.dumps(body))
