
with open('optimized_data_processor.py', 'r') as f:
    content = f.read()

# Make sure we use join pre-cache
content = content.replace("key = '.'.join(keys + [k]) if keys else k", "key = join_keys(keys + [k]) if keys else k")
content = content.replace("keys = []", "keys = []\n        join_keys = '.'.join")
with open('optimized_data_processor.py', 'w') as f:
    f.write(content)
