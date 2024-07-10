def add(a,b):
    return a+b

# create a poco with a simple int, string fields
class SimplePoco:
    def __init__(self, an_int, a_string):
        self.an_int = an_int
        self.a_string = a_string

# create a simple function that processes a list of these 
# pocos. If the list is empty, throw an exception. If
# a element is None then throw and exception
def process_list_of_pocos(pocos):
    if len(pocos) == 0:
        raise ValueError("List of pocos is empty")
    for poco in pocos:
        if poco is None:
            raise ValueError("Poco is None")
    return True