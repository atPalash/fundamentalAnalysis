def hello(data):
    res = f"Hello from discord you said {data}"
    return res


def add(data):
    val = data.split(",")
    val1 = float(val[0])
    val2 = float(val[1])
    res = val1 + val2
    return str(res)


route_methods = {
    "hello":    hello,
    "add":      add,
    }
