# # Image metadata
# # Metadata extraction
# # gps tracing on browser
# # metadata editing
# # metadata scrubbing
# # Excel file for image(s) metadata


# # IPTC International Press Telecommunications Council
# # EXIF exchangeable image format
# # XMP extensible Metadata format developed by adobe
# # Resource : ngtvspc/EXIF_remover.py
# # Resource : Pillow documentation
# # Resource : Image module documentation

# supporting imports
import os
import smtplib
import sys
from PIL import Image as im, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import csv
import pandas as pd
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

import gmplot

# declaring Global Variables
c_file = None               # c_file will store the filename
c_image = None              # object of Image class containing the image
cpath = None                # cpath stores the current working directory path
tag_dic = {}             # stores the final dictionary of tags (as keys) and data values
gps_dic = {}              # stores the dictionary associated with tag 'GPSInfo' in tag_dic
# latlong = None              # stores the formatted values of GPS co-ordinates
clean_image = None          # object of Image class that stores the scrubbed Image
i = 0

    # Option - 1 [Changing the directory]
    # Current working directory (cwd)
    # helps to fetch the file from file-path defined by user
    # checks if the user defined filepath exists
    # if TRUE then change the cwd to user defined path
    # cpath -> Current Path defined by user
    # working in cwd gives user a convenoience of not requiiring to enter the file_path

def menu():
    '''Diaplays main menu and accepts user inputs for the flow in program'''
    global i
    if i < 1:                   
        print("-"*40)
        i += 1
    else:
        pass

    print("*"*12, "Main Menu", "*"*12)
    option = int(input("""1: Change Current working Directory Address
2: Upload Image File
3: Extract Image Metadata
4: Create a clean copy (without metadata)
5: Exit
Enter the option number :  """))

    # to change cwd
    if option == 1:          
        print()
        change_cwd()

    # to upload an image
    elif option == 2:       
        print()
        import_image()

    # to extract metadata from image
    elif option == 3:
        
        # if image is not uploaded yet
        if c_image is None: 
            print("Upload image first.")
            import_image()
        else:
            # initialize extraction process if image already uploaded
            meta_extraction()       

    # creating a clean copy of the image by scrubbing the metadata
    elif option == 4:               
        if c_image is None:
            print("Please upload the image first.")
            import_image()
        else:
            # if image is already uploaded by the user
            create_copy()           

    # exit
    elif option == 5:           
        confirm = input("Are you sure you want to exit? (answer y or n) : ").upper()
        if confirm == "Y":
            stop()
        else:
            menu()

    else:
        print('Invalid Number')
        menu()



# Change the directory
# Option - 1
def change_cwd():
    '''Changes the current working directory for the convenience of user to upload the file'''

    print(12 * "-", "Changing CWD", 12 * "-")
    # getcwd() returns the path of cwd
    print("Current working directory : ", os.getcwd())    
    global cpath
    
    # dir path
    cpath=input("Enter the directory address where you want program's cwd in the format given below\n[/home/user/Desktop/folder_1/folder_4/folder_2/ ]\n: ")      

    # returns a boolean value 'TRUE' if the directory path exists
    if os.path.exists(cpath):
        # change cwd to the directory defined by user
        os.chdir(cpath)         
        print("Current Working Directory updated to : ", os.getcwd())
        print("Returning to Main Menu")
        print()
        menu()
    else:
        print("invalid directory. CWD is unchanged.\nCurrent Working Directory : ",os.getcwd())
        print("Restarting the module!")
        print()
        change_cwd()






# importing data
# Option - 2 - [Importing the image file]
def import_image():
    '''To import the image file'''
    print(12 * "-", "Select an Image file", 12 * "-")

    global c_file
    global c_image


     # checks if c_file is already created or not, if not then the whole function is executed, if yes then user input for c_file is skipped
    if (c_file is None) :      

        print("Your current working directory (cwd) is  : ", os.getcwd())

        userchk_cwd= input("Check the cwd above and confirm if target image file is in the same directory.\nAnswer y or n : ").upper()

        # if cwd is same as image directory then no need for directory path
        if userchk_cwd == "Y":    
            print("Great! Now you just have to enter the filename.")
            # user input -> name of the image file
            c_file = input("Enter the name of the Image file : ")  
            if ".jpg" not in c_file:
                c_file += ".jpg"

            # Creating Image object and accessing the file using the specified path
            c_image = im.open(c_file)
            # displaying the image uploaded to the user
            im._show(c_image)            

        elif userchk_cwd == "N":
            c_file = input("No Problem! Just enter the complete directory path "
                           "of the image file including file name in the following format :.\n"
                           "/home/user/Desktop/folder_1/folder_4/folder_2/Image_Metadata.jpg\n")
            # Creating Image object and accessing the file using the specified path
            c_image = im.open(c_file)
            # displaying the image uploaded to the user
            im._show(c_image)          

    else:
        pass

    # asking user to confirm the image file
    userchk_image = input(f"Is this the image file you have uploaded for metadata extraction (file_name: {c_file})?\nEnter 'Y' for yes or 'N' for no : ").upper()

    if userchk_image == "Y":
        print("Image uploaded Successfully. ")
        print()
        menu()

    elif userchk_image == "N":
        print("Restarting Image upload Module...")
        c_file = None
        print()
        import_image()

    else:
        print("Invalid option!")
        print()
        import_image()




# metadata extraction
# option - 3
def meta_extraction():
    '''Extraction of Data and writing it in .csv and .xlsx files'''
    print(12 * "-", "Extracting Metadata ", 12 * "-")
    global tag_dic
    global gps_dic
    global latlong
    global c_image

    # iterating over the values (exif tags/metadata) returned by getexif() from
    for tag, value in c_image._getexif().items():      

        # cross-referencing keys in tag_dic to that with the keys in TAGS dictionary
        if tag in TAGS:                               
            # print("TAGS[tag] : ",TAGS[tag])
            tag_dic[TAGS[tag]] = value

        else:
            pass

     # Replacing numerical tags of values in GPSInfo
    for key, value in tag_dic["GPSInfo"].items():

        # with corresponding standard GPSTAGS
        gps_dic[GPSTAGS[key]] = value                   

##    print("tag_dic : ", tag_dic)

    print("Data has been successfully extracted")

    features = list(tag_dic.keys())                                                                 # creating a list of all the keys in tag_dic
    metadata = open("exif_records.csv", "w")                                           # creating file object with filename as "exif_records.csv"
    record_write = csv.DictWriter(metadata, fieldnames=features)        # creating object of Dictwriter and setting column names
    record_write.writerow(tag_dic)                                                              # writing the extracted metadata as a row in the file
    metadata.close()                                                                                    # closing file
    print("exif_records.csv file updated")


    ## creating and updating excel file

    df = pd.read_csv("exif_records.csv", names=features)                        # using Pandas to create a data frame from the csv file
    df.to_excel('EXIF_records.xlsx', columns=features, index=False)     # using to_excel method to update the xlsx file

    print("The metadata has been stored successfully in the Excel file(.xlsx format) successfully.")
    menu()



# # # creating a copy of the image without EXIF data
# # option - 4
def create_copy():
    '''Creates a copy of the image without metadata'''
    print(12 * "-", "Scrubbing the metadata and creating a new image file with no metadata ", 12 * "-")
    global c_image
    global c_file
    global clean_image

    image_data = list(c_image.getdata())                                # returns pixel value of the image data as a sequence
    clean_image = im.new(c_image.mode, c_image.size)    # creates a new image with the given mode and size of original image
    clean_image.putdata(image_data)                                     # copies pixel data to clean_image
    clean_image.save(f"clean_{c_file}")                                     # saves the image with the given filename

    print(f"A clean copy of the image {c_file} without tags has been created Successfully.")
    print("Feel free to share the cleaned image over internet.")
    print("We enable anonymity.")
    print()
    menu()

# closing the program
# Option - 5
def stop():
    '''Terminates the program'''
    
    # terminates the program
    sys.exit()
    
menu()
