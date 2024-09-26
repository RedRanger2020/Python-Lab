
from Modules.DataMod import DataMod

def main():
    searchValues = ["cat","dog"]
    countAmount = 1000
    for value in searchValues:
        while True:
            if(DataMod.clearData(value)>=countAmount):
                break
            DataMod.imgSearch(value,countAmount);
              

if __name__ == '__main__':
    main()