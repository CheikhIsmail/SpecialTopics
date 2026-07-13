# ❌ Regex-Extraktion – absichtlich fragil
import re

antwort = """
Mein Name ist Maria Müller, ich bin 34 Jahre alt
und arbeite als Softwareentwicklerin.
"""

name  = re.search(r"Name ist (.+?),", antwort).group(1)
alter = re.search(r"(\d+) Jahre", antwort).group(1)
print(name, alter)  # Maria Müller 34

# Jetzt variieren wir den Prompt leicht...
antwort2 = "Die Entwicklerin Maria (34) stellt sich vor."
# → AttributeError: 'NoneType' object has no attribute 'group'
# Das Regex bricht. Genau das wollen wir zeigen.