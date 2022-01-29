from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Gastos_Solicitudes_Viaticos, Gastos_Viaticos_Desgloza, Receipt,Beneficiarios


proj_view = Blueprint('proj_view', __name__)

class Budget:
    def __init__(self):
        # self.item = [budget, proven, spent]
        self.hospedaje = [0,0,0]
        self.casetas = [0,0,0]
        self.desayuno = [0,0,0]
        self.hielo = [0,0,0]
        self.taxi = [0,0,0]
        self.tarjeta_telefonica = [0,0,0]
        self.lavanderia = [0,0,0]
        self.envios = [0,0,0]
        self.comida = [0,0,0]
        self.cena = [0,0,0]
        self.renta_auto = [0,0,0]
        self.avion = [0,0,0]
        self.agua_embotellada = [0,0,0]
        self.autobus = [0,0,0]
        self.combustible = [0,0,0]
        self.otros = [0,0,0]
        self.total = [0,0,0]
        self.error = [0,0,0]
        
class Status:
    def __init__(self):
        self.current = "Incompleto"

    def set_status(self, status):
        self.current = status

class Project:
    def __init__(self,project_id,budget,spent,proven, indicator):
        status = Status()
        self.project_id = project_id
        self.budget = round(budget,2)
        self.spent = round(spent,2)
        self.proven = round(proven,2)
        self.indicator = status
        self.indicator.set_status(indicator)

def project_list(user):
    projects = []
    try:
        numero_proveedor = Beneficiarios.query.filter_by(razon_social = user.name).first().numero_beneficiario
    except AttributeError:
        return projects

    gas_sol_2 = Gastos_Solicitudes_Viaticos.query.filter_by(numero_proveedor = numero_proveedor).all()
    
    for i in range(len(gas_sol_2)):
        if gas_sol_2[i].numero_orden != "0":
            spent = 0
            budget = 0
            proven = 0 
            a = Gastos_Viaticos_Desgloza.query.filter_by(viaticosidfk=gas_sol_2[i].numero_solicitud_viatico).all()
            for desgloza in a:
                budget += desgloza.importe + desgloza.complemento
                proven += desgloza.comprobado

            receipts = Receipt.query.filter_by(project_id=gas_sol_2[i].numero_orden, user=current_user).all()
            for receipt in receipts:
                spent += receipt.total + receipt.iva
            
            if spent <= proven:
                indicator = "Completo"
            else:
                indicator = "Incompleto"

            projects.append(Project(gas_sol_2[i].numero_orden, budget, spent, proven, indicator))

    return projects
        
        
@proj_view.route('/project_view',methods=["POST","GET"])
@login_required
def project_view():
    projects = project_list(current_user)
    projects.sort(key = lambda x: int(x.project_id), reverse=True)
    return render_template('project_view.html',projects=projects,user=current_user)


@proj_view.route('/budget/<int:project_id>', methods=["POST","GET"])
@login_required
def budget(project_id):
    receipts = Receipt.query.filter_by(project_id = project_id).all()

    ben = Beneficiarios.query.filter_by(razon_social = current_user.name).first()
    num_prov = ben.numero_beneficiario
    gast = Gastos_Solicitudes_Viaticos.query.filter_by(numero_proveedor = num_prov, numero_orden=project_id).first()
    breakdown = Gastos_Viaticos_Desgloza.query.filter_by(viaticosidfk=gast.numero_solicitud_viatico).all()
    budget_object = Budget()
    for item in breakdown:
        budget_object.total[0] += item.complemento + item.importe
        budget_object.total[1] += item.comprobado
        if item.nombre == 'hospedaje':
            budget_object.hospedaje[0] += item.complemento + item.importe
            budget_object.hospedaje[1] += item.comprobado
        elif item.nombre == 'casetas':
            budget_object.casetas[0] +=  item.complemento + item.importe
            budget_object.casetas[1] += item.comprobado
        elif item.nombre == 'desayuno':
            budget_object.desayuno[0] +=  item.complemento + item.importe
            budget_object.desayuno[1] += item.comprobado
        elif item.nombre == 'hielo':
            budget_object.hielo[0] +=  item.complemento + item.importe
            budget_object.hielo[1] += item.comprobado
        elif item.nombre == 'taxi':
            budget_object.taxi[0] +=  item.complemento + item.importe
            budget_object.taxi[1] += item.comprobado
        elif item.nombre == 'tarjeta_telefonica':
            budget_object.tarjeta_telefonica[0] +=  item.complemento + item.importe
            budget_object.tarjeta_telefonica[1] += item.comprobado
        elif item.nombre == 'lavanderia':
            budget_object.lavanderia[0] +=  item.complemento + item.importe
            budget_object.lavanderia[1] += item.comprobado
        elif item.nombre == 'envios':
            budget_object.envios[0] +=  item.complemento + item.importe
            budget_object.envios[1] += item.comprobado
        elif item.nombre == 'comida':
            budget_object.comida[0] +=  item.complemento + item.importe
            budget_object.comida[1] += item.comprobado
        elif item.nombre == 'cena':
            budget_object.cena[0] +=  item.complemento + item.importe
            budget_object.cena[1] += item.comprobado
        elif item.nombre == 'renta_auto':
            budget_object.renta_auto[0] +=  item.complemento + item.importe
            budget_object.renta_auto[1] += item.comprobado
        elif item.nombre == 'avion':
            budget_object.avion[0] +=  item.complemento + item.importe
            budget_object.avion[1] += item.comprobado
        elif item.nombre == 'agua_embotellada':
            budget_object.agua_embotellada[0] +=  item.complemento + item.importe
            budget_object.agua_embotellada[1] += item.comprobado
        elif item.nombre == 'autobus':
            budget_object.autobus[0] +=  item.complemento + item.importe
            budget_object.autobus[1] += item.comprobado
        elif item.nombre == 'combustible':
            budget_object.combustible[0] +=  item.complemento + item.importe
            budget_object.combustible[1] += item.comprobado
        elif item.nombre == 'otros':
            budget_object.otros[0] +=  item.complemento + item.importe
            budget_object.otros[1] += item.comprobado
        else: 
            budget_object.error[0] +=  item.complemento + item.importe
            budget_object.error[1] += item.comprobado

    for receipt in receipts:
        if 'hospedaje' == receipt.cost:
            budget_object.hospedaje[2] += receipt.total + receipt.iva
        elif 'casetas' == receipt.cost:
            budget_object.casetas[2] += receipt.total + receipt.iva
        elif 'desayuno' == receipt.cost:
            budget_object.desayuno[2] += receipt.total + receipt.iva
        elif 'hielo' == receipt.cost:
            budget_object.hielo[2] += receipt.total + receipt.iva
        elif 'taxi' == receipt.cost:
            budget_object.taxi[2] += receipt.total + receipt.iva
        elif 'tarjeta_telefonica' == receipt.cost:
            budget_object.tarjeta_telefonica[2] += receipt.total + receipt.iva
        elif 'lavanderia' == receipt.cost:
            budget_object.lavanderia[2] += receipt.total + receipt.iva
        elif 'envios' == receipt.cost:
            budget_object.envios[2] += receipt.total + receipt.iva
        elif 'comida' == receipt.cost:
            budget_object.comida[2] += receipt.total + receipt.iva
        elif 'cena' == receipt.cost:
            budget_object.cena[2] += receipt.total + receipt.iva
        elif 'renta_auto' == receipt.cost:
            budget_object.renta_auto[2] += receipt.total + receipt.iva
        elif 'avion' == receipt.cost:
            budget_object.avion[2] += receipt.total + receipt.iva
        elif 'agua_embotellada' == receipt.cost:
            budget_object.agua_embotellada[2] += receipt.total + receipt.iva
        elif 'autobus' == receipt.cost:
            budget_object.autobus[2] += receipt.total + receipt.iva
        elif 'combustible' == receipt.cost:
            budget_object.combustible[2] += receipt.total + receipt.iva
        elif 'otros' == receipt.cost:
            budget_object.otros[2] += receipt.total + receipt.iva


    return render_template('budget.html',budget=budget_object)