from dataclasses import dataclass, field


def my_list() -> list:
    return []


@dataclass
class Foo:
    my_list: list[str] = field(default_factory=my_list)


another_list = []
f = Foo(another_list)
f.my_list.append('a')
f.my_list.append('b')
f.my_list.append('c')

print(f.my_list)

print(another_list)


