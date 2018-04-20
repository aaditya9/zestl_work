def main():

    with open("adt-eg1.txt","r") as rf:
        data=rf.read()
        print (data.strip())


if __name__=="__main__":
    main()