from yattag import Doc
import json
doc, tag, text = Doc().tagtext()
serialized_rows = [{"name": "Test <script>alert(1)</script>"}]
with tag('script', id="data-test", type="application/json"):
    doc.asis(json.dumps(serialized_rows))
print(doc.getvalue())
