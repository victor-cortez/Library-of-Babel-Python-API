import pybel

# Gets a book from the library
a = pybel.browser("hello",1,1,1,1)
# Prints the entire book
print(a)

# Returns 4 results for searching the string "hello" in the library
c = pybel.search("hello")
print(c)
print(c[0].hexagon)

# Returns a random book
r = pybel.random()
print(r)