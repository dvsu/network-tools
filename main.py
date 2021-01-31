from datetime import datetime
from subprocess import check_output


if __name__ == "__main__":
    result = check_output(['ping', 'www.google.com'])
    print(result)