def add(*args):
    """
    Add two number. input argument is split into separate numbers using ","
    e.g.:
    add: 10, 20
    Keyword arguments:
    data -- numbers separated by ","
    """
    val = args[0].split(",")
    val1 = float(val[0])
    val2 = float(val[1])
    res = val1 + val2
    return str(res)


def commands(*args):
    """
    List all methods which can be queried from Discord.
    e.g.:
    commands: all -> list all command api.
    commands: <command> -> shows spi for specified command.
    Keyword arguments:
    data -- numbers separated by ","
    """
    res = ""
    if args[0] == "all":
        for method, func in route_methods.items():
            res += f"{method}:{func.__doc__}\n"
    else:
        if route_methods.get(args[0]) is not None:
            res = route_methods[args[0]].__doc__
        else:
            res = "This method is not available, check all methods available commands: all"

    return res


def hello(*args):
    """
    Says hello to user.
    e.g.
    hello: user
    Keyword arguments:
    data -- any user input
    """
    res = f"Hello from discord you said {args[0]}"
    return res


route_methods = dict(add=add, commands=commands, hello=hello)
