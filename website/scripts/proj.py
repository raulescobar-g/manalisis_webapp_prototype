#blueprint for project selection
from .models import Ordenes_Muestreo_2
from flask import Blueprint, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from .proj_view import project_list 


proj = Blueprint('proj', __name__)

#MAKES NEW PROJECT OR CONTINUES EXISTING ONE
@proj.route('/project_selection',methods=['POST','GET'])
@login_required
def project_selection():
    project_name = request.form['project_name']
    match = False
    list_projects = project_list(current_user)
    for project in list_projects:
        if project.project_id == project_name:
            match = True
            break
    
    if match == False:
        flash("Usuario no esta asignado a esta OT","info")
        return redirect(url_for('views.index'))
            
    project_id = Ordenes_Muestreo_2.query.filter_by(id = int(project_name)).first()
    
    

    if project_id is None:
        flash("Orden de Trabajo no existe en nuestra base de datos","info")
        return redirect(url_for('views.index'))

    session['project_id'] = project_id.id
    session.permanent = True
    return redirect(url_for('views.index'))


@proj.route('/project_change',methods=['POST','GET'])
@login_required
def project_change():
    session.pop('project_id',None)
    return redirect(url_for('views.index'))
