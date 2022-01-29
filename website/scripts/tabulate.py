from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Receipt, XML
from .. import db
from .helper import fetch_file, img_delete
import base64


tabulate = Blueprint('tabulate', __name__)


@tabulate.route('/table/<int:project_id>',methods=["POST","GET"])
@login_required
def table(project_id):
    receipts = Receipt.query.filter_by(user=current_user,project_id = project_id).all()
    
    if len(receipts) == 0:
        flash("No hay recibos con esos parametros",'info')
    
    xml = XML.query.all()

    return render_template('table.html',receipts=receipts,xml=xml)



#TOOL FOR DELETEING RECEIPTS
@tabulate.route('/table/delete/<int:receipt_id>')
def delete_task(receipt_id):
    task_to_del = Receipt.query.get_or_404(receipt_id)
    xml = XML.query.filter_by(receipt_id_xml = receipt_id).first()
    if xml is not None:
        flash("No se pueden borrar gastos que ya fueron comprobados",'info')
        return redirect(url_for("tabulate.table",project_id=task_to_del.project_id))
    if task_to_del.file_loc is not None:
        img_delete(task_to_del.file_loc)
    
    try:
        #try to delete image from folder as it takes up space
        db.session.delete(task_to_del)
        db.session.commit()
        flash("Recibo fue eliminado",'info')
        return redirect(url_for("tabulate.table",project_id=task_to_del.project_id))
    except:
        return 'Error deleteing task'
        

@tabulate.route('/table/show_img/<int:receipt_id>',methods=["POST","GET"])
@login_required
def show_img(receipt_id):
    file_loc = Receipt.query.filter_by(receipt_id=receipt_id).first().file_loc
    im = fetch_file(file_loc,'/images/')
    encoded_img_data = base64.b64encode(im.getvalue())
    return render_template('image.html',img=encoded_img_data.decode('utf-8'))




@tabulate.route('/table/show_xml/<int:receipt_id>',methods=["POST","GET"])
@login_required
def show_xml(receipt_id):
    xml = XML.query.filter_by(receipt_id_xml=receipt_id).first().file_loc
    file = fetch_file(xml,'/xml/')
    return render_template('xml.html',xml=file.read().decode('utf-8'))

