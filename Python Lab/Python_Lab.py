
from Modules.DataMod import DataMod

def main():
    search_values = ["cat","dog"]
    count_amount = 1000
    for value in search_values:
        while True:
            if(DataMod.clear_data(value)>=count_amount):
                break
            DataMod.img_search(value,count_amount);
              

if __name__ == '__main__':
    main()