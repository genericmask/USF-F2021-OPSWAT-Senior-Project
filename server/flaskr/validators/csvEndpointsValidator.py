import csv

CSV_MINIMUM_ROW_COUNT = 2
CSV_MAXIMUM_ROW_COUNT = 25
IP_ERROR_BASE_MESSAGE = "Expected a set of four numbers separated by '.' where each number in the set can range from 0 to 255. \nInvalid IP address: "

# @param=csv : A TextIOWrapper stream that contains a csv file. 
# Checks if csv has two columns: "Endpoint IP" and "Accessible"
# Also checks that all "accessible" values are bool and endpoint IPs are valid
# @return : None if the csv is valid. If invalid, a string containing the error
def csvEndpointsValidator(csvfile):
    reader = csv.reader(csvfile)
    csv_arr = [row for row in reader]

    if len(csv_arr) < 1:
        return "File is empty."
    if len(csv_arr) < 2:
        return "Expected more than one line."
    if len(csv_arr) < CSV_MINIMUM_ROW_COUNT + 1: # +1 for the column names
        return "File contains " + str(len(csv_arr)) + "rows. Minimum accepted rows: " + " " + str(CSV_MINIMUM_ROW_COUNT)
    if len(csv_arr) > CSV_MAXIMUM_ROW_COUNT + 1:
        return "File contains " + str(len(csv_arr)) + "rows. Maximum accepted rows: " + " " + str(CSV_MAXIMUM_ROW_COUNT)

    if csv_arr[0][0].lower().count("ip") < 1:
        return "Expected first column to be 'Endpoint IP', it was: " + csv_arr[0][0]
    if csv_arr[0][1].lower().count("accessible") < 1:
        return "Expected second column to be 'Accessible', it was: " + csv_arr[0][1]
    csv_arr.pop(0) # Remove the column names since they're valid
    
    for x in csv_arr:
        # Check the ip address, it should be IPv4 and contain a set of four numbers
        ip_nums = x[0].strip().split(".")
        if len(ip_nums) != 4:
            return IP_ERROR_BASE_MESSAGE + x[0]
        for num in ip_nums:
            if not num.isnumeric() or int(num) < 0 or int(num) > 255:
                return IP_ERROR_BASE_MESSAGE + x[0]
        
        # Check the accessible value, trues must be TRUE and false FALSE
        accessible_val = x[1]
        if accessible_val != "TRUE" and accessible_val != "FALSE":
            return "The Accessible value '" + accessible_val + "' is unacceptable. \nAcceptable values for the Accessible column are: 'TRUE' and 'FALSE'."
    
    return None

