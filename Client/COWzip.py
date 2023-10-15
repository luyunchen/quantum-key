

def zip(folder, zipName):
    import shutil
    shutil.make_archive(zipName, 'zip', folder)

def unzip (zipName, folder):
    import shutil
    shutil.unpack_archive(zipName, folder, 'zip')