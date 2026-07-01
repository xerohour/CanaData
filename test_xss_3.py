from yattag import Doc
import json
doc, tag, text = Doc().tagtext()
serialized_rows = [{"name": "Test </script><script>alert(1)</script>"}]
json_str = json.dumps(serialized_rows).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
with tag('script', id="data-test", type="application/json"):
    doc.asis(json_str)
print(doc.getvalue())
