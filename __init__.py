
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

    sha=__get_sha_master(packagename)
    
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

    import os
    with open(os.path.join(path,packagename,".sha"),'w') as f:
        f.write(sha)
    
    
    return True

def __import(packagename):
    import importlib
    globals()[packagename]=importlib.import_module('purpys.'+packagename)
    return True

def install(packagename):
    import os
    import shutil
    
    if os.path.exists(os.path.join(__get_module_path(), packagename)):
        if has_update(packagename):
            print("There is an update available for this package.")
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

def __get_sha_master(packagename):
    import json
    import urllib.request as R
    version_response = R.urlopen('https://api.github.com/repos/purpys/'+packagename+'/branches/master')
    version = version_response.read()
    d=json.loads(version.decode('UTF-8'))
    sha=d["commit"]["sha"]    
    return sha

def __sha_path(packagename):
    import os
    return os.path.join(__get_module_path(), packagename, ".sha")

def __read_sha(packagename):
    import os
    with open(__sha_path(packagename),'r') as f:
        return f.read()

def has_update(packagename):
    sha=__read_sha(packagename)
    sha2=__get_sha_master(packagename)
    return sha!=sha2
    
def update(packagename):
    if has_update(packagename):
        print("Updating package to newest version")
        uninstall(packagename)
        return install(packagename)
    else:
        print("Package is already newest version")
    
def uninstall(packagename):
    import os
    import shutil
    return shutil.rmtree(os.path.join(__get_module_path(), packagename))

def test_import():
    global os
    import os

if __name__=="__main__":
    print("This script cannot be run, it must be imported.")
