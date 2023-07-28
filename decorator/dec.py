import time


def is_admin(func):
    def wrapper(*args, **kwargs):
        try:
            user_type = kwargs.get('user_type', None)
            if user_type == 'admin':
                return func(*args, **kwargs)
            raise ValueError()
        except ValueError:
            return 'Value error: Permission denied'
    return wrapper


@is_admin
def show_customer_receipt(user_type: str):
    return f'Pass as {user_type}'


def catch_errors(func):
    def wrapper(*args, **kwargs):
        try:
            print()
            func(*args)
        except KeyError:
            for el in args:
                for k, v in el.items():
                    print(
                        f'Found 1 error during execution of your function: KeyError no such key as {k}')
    return wrapper


@catch_errors
def print_key_value(data: dict):
    print(data['key'])


def check_types(func):
    def wrapper(*args, **kwargs):
        try:
            for el in args:
                if not isinstance(el, int):
                    raise TypeError(type(el))
            return func(*args)
        except TypeError as e:
            return f"TypeError: Argument must be <class 'int'> not {e.args[0]}"

    return wrapper


@check_types
def add(a: int, b: int) -> int:
    return a + b


def cache_result(func):
    cache = {}

    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@cache_result
def calculation(x: int or float):
    print(f"Calculating for {x}")
    return pow(x, 3)


def limiter(max_calls: int, period_in_seconds: int):
    def decorator_limiter(func):
        call_time = []

        def wrapper(*args, **kwargs):
            current_time = time.time()

            while call_time and call_time[0] <= current_time - period_in_seconds:
                call_time.pop(0)
            if len(call_time) < max_calls:
                call_time.append(current_time)
                print(call_time)
                return func(*args, **kwargs)
            else:
                raise Exception(
                    f"Rate limit exceeded. You can only call this function {max_calls} times per {period_in_seconds} seconds.")
        return wrapper
    return decorator_limiter


@limiter(5, 60)
def limited_func(x):
    print(f"Function called with argument: {x}")
    return x * 4
