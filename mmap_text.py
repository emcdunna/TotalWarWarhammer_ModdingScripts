import mmap

# write a simple example file
with open("hello.txt", "wb") as f:
    f.write(b"Hello Python!\n")

with open("hello.txt", "r+b") as f:
    mm = mmap.mmap(f.fileno(),0)
    print mm.readline()
    print mm.readline()
    print mm.readline()
