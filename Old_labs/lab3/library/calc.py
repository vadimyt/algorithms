def Function(input):
    a=input[0]
    b=input[1]
    h=input[2]
    k=input[3]
    m=input[4]
    result = []
    while a <= b:
        x=a
        result.append(k*x+m)
        a+=h
    return result