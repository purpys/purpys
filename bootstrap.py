def get():

    packagename = 'purpys'
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
                i.filename=i.filename.split(packagename+'-master')[1]

    path=".."

    for i in l:
        if packagename+'-master' in i:
            if i.split(packagename+'-master')[1]:
                z.extract(i, path)

    z.close()
