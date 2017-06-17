
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

def __get_available_packages():
    import urllib.request as R
    import json
    preresponse=R.urlopen('https://api.github.com/orgs/purpys/repos')
    names=[i["name"] for i in json.loads(preresponse.read().decode('UTF-8'))]
    return names

def exists(packagename):
    return packagename in __get_available_packages()

def download(packagename):
    import urllib.request as R
    import io as I
    import zipfile as Z

    if not exists(packagename):
        print("ERROR: Package does not exist")
        return False
    
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

def is_installed(packagename):
    import os
    return os.path.exists(os.path.join(__get_module_path(), packagename))

def is_downloaded(packagename):
    import os
    return os.path.exists(os.path.join(__get_cache_path(),packagename))

def install(packagename):
    import shutil, os
    
    if is_installed(packagename):
        if has_update(packagename):
            print("There is an update available for this package.")
        return __import(packagename)
    
    if is_downloaded(packagename):
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
    
    if is_downloaded(packagename):
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

def run(packagename, args=[]):
    if is_installed(packagename):
        __import(packagename)
        return globals()[packagename].main(args)
    else:
        print("ERROR: Cannot run package, because it is not installed")
    

if __name__=="__main__":
    print("This script cannot be run, it must be imported.")
    import sys
    print(sys.argv)
    action=None if len(sys.argv)<2 else sys.argv[1]
    package=None if len(sys.argv)<3 else sys.argv[2]
    pargs=sys.argv[3:]

    if action=='run':
        run(package, pargs)
    elif action=='update':
        update(package)
    elif action=='install':
        install(package)
    elif action=='available':
        for n in __get_available_packages():
            print(n)
    elif action=='uninstall':
        uninstall(package)
