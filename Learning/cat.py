def main():
    n = int(input("Enter a number: "))
    paint_column(n)

def paint_column(x):
    for _ in range(x):
        print("#")

main()