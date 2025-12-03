def cli_coords_input():

    x = 0
    y = 0

    print("Please input the coordinates of your move")

    while x < 1 or x > 8 :
        print("Input the x coordinate")

        try:
            x = int(input())
        except ValueError:
            print("Not an integer between 1-8 inclusive")
            x = 0

    while y < 1 or y > 8:
        print("Input the y coordinate")

        try:
            y = int(input())
        except ValueError:
            print("Not an integer between 1-8 inclusive")
            y = 0
        

    return (x,y)
