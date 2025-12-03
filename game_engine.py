def cli_coords_input():

    x = 0
    y = 0

    print("Please input the coordinates of your move")

    while x < 1 or x > 8 :
        print("Input the x coordinate")

        x = int(input())

    while y < 1 or y > 8:
        print("Input the y coordinate")
        
        y = int(input())

    return (x,y)



cli_coords_input()