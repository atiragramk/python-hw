from dec import (
    show_customer_receipt,
    print_key_value,
    add,
    calculation,
    limited_func
)


user_pass = show_customer_receipt(user_type='admin')
print(user_pass)


print_key_value({'foo': 'bar'})
print_key_value({'key': 'bar'})

print(add(1, 2))
print(add("1", "2"))

print(calculation(3))
print(calculation(3))
print(calculation(4))
print(calculation(5.5))
print(calculation(4))


for i in range(5):
    try:
        print(limited_func(i))
    except Exception as e:
        print(e)


for i in range(10):
    try:
        print(limited_func(i))
    except Exception as e:
        print(e)
