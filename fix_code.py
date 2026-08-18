with open("optimized_data_processor.py", "r") as f:
    content = f.read()

content = content.replace("""        # Cache locals for performance
        _isinstance = isinstance
        _dict = dict
        _list = list

        # Use iterative approach with explicit stack
        stack = [iter(d.items())]
        keys = []

        while stack:
            for k, v in stack[-1]:
                key = ".".join(keys + [k]) if keys else k

                if _isinstance(v, _dict):
                    # Push nested dict to stack
                    keys.append(k)
                    stack.append(iter(v.items()))
                    break
                elif _isinstance(v, _list):
                    if v and _isinstance(v[0], _dict):""", """        # Use iterative approach with explicit stack
        stack = [iter(d.items())]
        keys = []

        while stack:
            for k, v in stack[-1]:
                key = ".".join(keys + [k]) if keys else k

                if isinstance(v, dict):
                    # Push nested dict to stack
                    keys.append(k)
                    stack.append(iter(v.items()))
                    break
                elif isinstance(v, list):
                    if v and isinstance(v[0], dict):""")

content = content.replace("""        # Cache types for fast_convert
        _float = float
        _int = int

        def fast_convert(val):
            if val is None or val == "None":
                return val
            try:
                f = _float(val)
                i = _int(f)
                return i if i == f else f
            except (ValueError, TypeError):
                return val

        # Convert data types where possible
        for col in df.columns:
            # Try to convert to numeric where possible. Carefully constrain to avoid coercing string IDs.
            if (
                "price" in col.lower()
                or "amount" in col.lower()
                or "thc" in col.lower()
            ):
                df[col] = [fast_convert(x) for x in df[col].to_numpy()]""", """        # Convert data types where possible
        for col in df.columns:
            # Try to convert to numeric where possible. Carefully constrain to avoid coercing string IDs.
            if (
                "price" in col.lower()
                or "amount" in col.lower()
                or "thc" in col.lower()
            ):
                original_col = df[col]
                numeric_col = pd.to_numeric(original_col, errors="coerce")
                df[col] = numeric_col.where(numeric_col.notna(), original_col)""")

with open("optimized_data_processor.py", "w") as f:
    f.write(content)
