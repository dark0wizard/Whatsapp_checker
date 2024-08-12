import datetime
import csv


def write_data_in_csv(data):
    '''This function saves info about WhatsApp account in a csv file'''
    today_date = datetime.datetime.now()
    filename = today_date.strftime("%Y-%m-%d_%H-%M") + ".csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Phone number", "Whatsapp", "About", "Picture"])
        writer.writerows(data)


def read_phone_numbers_from_txt(file_path: str) -> list[str]:
    '''This function reads phone numbers from a .txt file'''
    with open(file_path, 'r') as file:
        numbers = [line.strip() for line in file if line.strip()]
    return numbers