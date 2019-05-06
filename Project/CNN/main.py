

# file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"

import sys
sys.path.insert(0, '../newupload')
from service.file_service import file_info

def main():
    file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"
    print(file_info(file_path))
    return 

if __name__ == '__main__':
    main()