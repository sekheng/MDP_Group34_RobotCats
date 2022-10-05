import shutil
import os
from time import sleep
import paramiko
from paramiko.ssh_exception import SSHException
from datetime import datetime


def get_image_results():

    rpiServer = "192.168.34.34"
    rpiUsername = "pi"
    rpiPassword = "raspberry34"

    rpiImageDirectory = "./Desktop/rpi/images"
    imageDirectory = "C:/Users/cheyj/Desktop"
    results_dir = "resultsFolder"
    backupDirectory = "backupImageFolder"

    createFolders = [imageDirectory, results_dir, backupDirectory]

    for fldr in createFolders:
        if not os.path.exists(fldr):
            os.makedirs(fldr)


    #connect to rpi
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(rpiServer, 22, rpiUsername, rpiPassword)
    sftp = ssh.open_sftp()


    print("\n Connected to RPI\n")

    filename = f"results_{datetime.now()}.jpg"
    remotepath = rpiImageDirectory + "/" + filename
    #rename the image files
    localFilePath = os.path.join(imageDirectory, filename + "-temporary")
    sftp.get(remotepath, localFilePath, callback=None)
    print("Transfering " + filename + "...")
    newLocalFilePath = localFilePath.replace("-temporary","")
    os.rename(localFilePath, newLocalFilePath)
    backupFilePath = os.path.join(backupDirectory, filename)
    shutil.copy2(newLocalFilePath, backupFilePath)
    print("done!")