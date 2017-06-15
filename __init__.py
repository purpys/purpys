
def read_config():
    pass

def dump_config():
    pass

def __get_module_path():
    return __path__[0]

def __get_cache_path():
    import os
    return os.path.join(__get_module_path(),'.cache')

def __create_cache_dir():
    import os
    os.mkdir(__get_cache_path())

def download(packagename):
    import urllib.request as R
    import io as I
    import zipfile as Z
    
    response = R.urlopen('https://github.com/purpys/'+packagename+'/archive/master.zip') #TODO: Implement versioning
    zipcontent = response.read()
    s=I.BytesIO(zipcontent)
    try:
        z=Z.ZipFile(s,'r')
    except Z.BadZipfile:
        print("Zip extraction failed!")
        raise

    l=z.namelist()

    for i in z.filelist:
        if packagename+'-master' in i.filename:
            if i.filename.split(packagename+'-master')[1]:
                i.filename=packagename + '/' + i.filename.split(packagename+'-master')[1]

    path=__get_cache_path()

    for i in l:
        if packagename+'-master' in i:
            if i.split(packagename+'-master')[1]:
                z.extract(i, path)

    z.close()
    return True

def __import(packagename):
    import importlib
    globals()[packagename]=importlib.import_module('purpys.'+packagename)
    return True

def install(packagename):
    import os
    import shutil
    
    if os.path.exists(os.path.join(__get_module_path(), packagename)):
        return __import(packagename)
    
    if os.path.exists(os.path.join(__get_cache_path(),packagename)):
        shutil.move(os.path.join(__get_cache_path(),packagename),os.path.join(__get_module_path(), packagename))
        return __import(packagename)
    else:
        if download(packagename):
            shutil.move(os.path.join(__get_cache_path(),packagename),os.path.join(__get_module_path(), packagename))
            return __import(packagename)
        else:
            print("ERROR:\tDownloading package failed!")

#Bug: Issue 1: Does not properly override previous installation
def reinstall(packagename):
    import os
    import shutil
    
    if os.path.exists(os.path.join(__get_cache_path(),packagename)):
        shutil.move(os.path.join(__get_cache_path(),packagename),os.path.join(__get_module_path(), packagename))
        return __import(packagename)
    else:
        if download(packagename):
            shutil.move(os.path.join(__get_cache_path(),packagename),os.path.join(__get_module_path(), packagename))
            return __import(packagename)
        else:
            print("ERROR:\tDownloading package failed!")    
    
def uninstall(packagename):
    import os
    import shutil
    return shutil.rmtree(os.path.join(__get_module_path(), packagename))

def test_import():
    global os
    import os

if __name__=="__main__":
    print("This script cannot be run, it must be imported.")
