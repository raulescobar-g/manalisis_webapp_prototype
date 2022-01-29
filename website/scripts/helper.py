import ftplib
import io
import xml.etree.ElementTree as et
from datetime import datetime
from .models import Receipt, manalisis_Users, Beneficiarios
username = "removed"
user = "removed"
password = "removed"
def file_upload(file,filename,UPLOAD_FOLDER):
    ftp = ftplib.FTP(username,user,password )
    localfile = UPLOAD_FOLDER + filename
    ftp.storbinary('STOR %s' % localfile, file)
    ftp.close()

def img_delete(filename):
    ftp = ftplib.FTP(username,user,password )
    img_file = '/images/'+filename
    ftp.delete(img_file)

def xml_delete(filename):
    ftp = ftplib.FTP(username,user,password )
    xml_file = '/xml/' + filename
    ftp.delete(xml_file)

def xml_uploader(current_user, xml_file):
    now = datetime.now()
    filename = str(current_user.id) + now.strftime("_%m.%d.%Y_%H.%M.%S")+ '.xml'
    xml_file.seek(0)
    file_upload(xml_file,filename,'/xml/')
    return filename

def fetch_file(filename,UPLOAD_FOLDER):
    ftp = ftplib.FTP(username,user,password )
    localfile = UPLOAD_FOLDER + filename
    file = io.BytesIO()
    ftp.retrbinary('RETR %s' % localfile, file.write)
    ftp.close()
    file.seek(0)
    return file

def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def xml_extractor(xml_file):
    tree = et.parse(xml_file)
    root = tree.getroot()
    data = root
    date = data.attrib['Fecha'][:10]
    total = float(data.attrib['SubTotal'])
    rfc = None
    iva = None
    for child in data:
        if 'Emisor' in child.tag and rfc is None:
            rfc = child.attrib['Rfc']
        if 'Impuestos' in child.tag and iva is None:
            iva = child.attrib['TotalImpuestosTrasladados']

    return date,total,rfc,iva

def names_list(nam):
    names = []
    search = "%{}%".format(nam.upper())
    a = Beneficiarios.query.filter(Beneficiarios.razon_social.ilike(search)).all()
    b = manalisis_Users.query.all()
    for name in a:
        if name.razon_social not in names:
            names.append(name.razon_social)

    for people in b:
        if people.name in names:
            names.remove(people.name)
            
    return names
