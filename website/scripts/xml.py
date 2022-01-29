#blueprint for xml files
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Gastos_Viaticos_Desgloza, Receipt, XML, Beneficiarios, Gastos_Solicitudes_Viaticos
from .. import db
from .helper import fetch_file, xml_extractor, xml_uploader, allowed_file

xml = Blueprint('xml', __name__)

ALLOWED_EXTENSIONS = set(['xml'])

@xml.route('/xml_upload',methods=['POST','GET'])
@login_required
def xml_upload():
    
    if request.method == 'POST':
        session['success'] = False
        xml_file = request.files["xml_input"]

        if not allowed_file(xml_file.filename,ALLOWED_EXTENSIONS):
            flash("Tiene que ser file tip .xml",'error')
            return redirect(url_for('xml.xml_upload'))

        date,total,rfc,iva = xml_extractor(xml_file)

        #change from first to all to handle collisions
        receipt = Receipt.query.filter_by(time=date, rfc=rfc, total=total,iva=iva).all()
        xmls = XML.query.all()
        for x in xmls:
            try:
                receipt.remove(x.receipt)
            except:
                pass
    
        if (len(receipt) >= 2) or (len(receipt) == 0) or (rfc is None) or (total is None) or (date is None) or (iva is None) or (receipt is None):
            filename = xml_uploader(current_user,xml_file)
            session['xml_file'] = filename
            return redirect(url_for("xml.xml_success"))

        
        filename = xml_uploader(current_user,xml_file)
    
        xml = XML(rfc=rfc,iva=iva,date=date,total=total,receipt=receipt[0],file_loc=filename)

        numero_proveedor = Beneficiarios.query.filter_by(razon_social = current_user.name).first().numero_beneficiario
        gas_sol_2 = Gastos_Solicitudes_Viaticos.query.filter_by(numero_proveedor = numero_proveedor,numero_orden=receipt[0].project_id).first()
        a = Gastos_Viaticos_Desgloza.query.filter_by(viaticosidfk = gas_sol_2.numero_solicitud_viatico,nombre=receipt[0].cost).first()
        a.comprobado += total + float(iva)
        
        db.session.add(xml)
        db.session.commit()
        session['success'] = True
        return redirect(url_for('xml.xml_success'))

    else:
        return render_template("xml_upload.html")


@xml.route('/xml_success',methods=['POST','GET'])
@login_required
def xml_success():
    if 'success' in session:
        success = session['success']
        receipts = Receipt.query.all()

        if success == False and 'xml_file' in session: 
            if request.method == 'POST':
                filename = session["xml_file"]
                
                match = request.form['receipt_id']
                receipt = Receipt.query.filter_by(receipt_id=match).first()

                xml_file = fetch_file(filename, '/xml/')
                xml_file.seek(0)
                date,total,rfc,iva = xml_extractor(xml_file)

                xml = XML(rfc=rfc,
                        date=date,
                        iva=iva,
                        total=total,
                        file_loc = filename,
                        receipt=receipt)


                numero_proveedor = Beneficiarios.query.filter_by(razon_social = current_user.name).first().numero_beneficiario
                gas_sol_2 = Gastos_Solicitudes_Viaticos.query.filter_by(numero_proveedor = numero_proveedor,numero_orden=receipt.project_id).first()
                a = Gastos_Viaticos_Desgloza.query.filter_by(viaticosidfk = gas_sol_2.numero_solicitud_viatico,nombre=receipt.cost).first()
                a.comprobado += total + float(iva)

                db.session.add(xml)
                db.session.commit()
                success = True
                session.pop('xml_file',None)
                return redirect(url_for('xml.xml_upload'))
            else:
                xmls = XML.query.all()
                for xml in xmls:
                    receipts.remove(xml.receipt)
                        
                return render_template("xml_success.html",success=success,receipts=receipts)
        else:
            flash("File xml fue agregado",'success')
            session.pop('success',None)
            return redirect(url_for('xml.xml_upload'))
    else:
        flash("Session timeout",'info')
        return redirect(url_for("auth.login"))




