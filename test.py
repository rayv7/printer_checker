import printersList
import time

def main():
    printersList.get_printer_list()
    target_ip = input("Enter ip or choose from listed: ")
    time.sleep(2)
    listed_ip = printersList.map_to_printer(target_ip)
    print(listed_ip)
    


if __name__ == "__main__":
    main()