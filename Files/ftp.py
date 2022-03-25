import ftplib
import os

ftp = ftplib.FTP('ftpAdress')
ftp.login('ftpUser','ftpPassowrd')

# Extract - Copy files from ftp server to working directory
files_ftp = []
files_ftp = ftp.nlst()

files_to_copy = [x for x in files_ftp]

for _, filename in enumerate(files_to_copy):
            ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)

ftp.quit() 