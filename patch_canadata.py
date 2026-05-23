with open('CanaData.py', 'r') as f:
    content = f.read()

content = content.replace("""        result = {}
        stack = [iter(d.items())] # Stack contains iterators of dictionary items
        keys = []                 # Tracks the current path in the dictionary (e.g., ['price', 'amount'])
        while stack:
            for k, v in stack[-1]:
                keys.append(k)
                if isinstance(v, list):""", """        result = {}
        stack = [iter(d.items())] # Stack contains iterators of dictionary items
        keys = []                 # Tracks the current path in the dictionary (e.g., ['price', 'amount'])
        join_keys = '.'.join
        while stack:
            for k, v in stack[-1]:
                keys.append(k)
                if isinstance(v, list):""")

content = content.replace("len(v.keys()) < 1", "not v")
content = content.replace("len(item.keys()) < 1", "not item")
content = content.replace("len(v) > 0", "v")
content = content.replace("'.'.join(keys)", "join_keys(keys)")
content = content.replace("'.'.join(item)", "join_keys(item)")
content = content.replace("'.'.join(str(x) for x in v)", "join_keys(str(x) for x in v)")

with open('CanaData.py', 'w') as f:
    f.write(content)
