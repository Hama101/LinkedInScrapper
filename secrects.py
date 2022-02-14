import random
#get a random line from keys.txt than split it by ; and strip it
EMAIL , PASSWORD = "" , ""

with open('keys.txt' , 'r') as f:
    #get a random line
    line = random.choice(f.readlines())
    line = line.strip()
    #split it by ;
    EMAIL , PASSWORD = line.split(';')


if __name__ == '__main__':
    print("email: ",EMAIL)
    print("password: ",PASSWORD)