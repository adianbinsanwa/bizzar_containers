from src import list_types as lt
from pytest import raises, fixture, mark


def gen(name, *args): return lt[name](*args)




