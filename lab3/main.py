m = 10
k=3

def Func(a=-5,b=5,h=0.25):
    result=[]
    n=1
    while a <= b:
        x=a
        F=k*x+m
        result.append([n,x,F])
        n+=1
        a+=h
    return result

if __name__ == "__main__":
    #a = float(input())
    #b = float(input())
    #h = float(input())        
    #res=Func(a,b,h)
    res=Func()
    print("№"+" "+"X"+" "+"F(x)")
    for i in range(len(res)-1):
        print(str(res[i][0])+" "+str(res[i][1])+" "+str(res[i][2]))