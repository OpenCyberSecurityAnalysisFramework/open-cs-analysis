from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm, EmployeeAssignForm, RoleForm, AttackerForm
from .. import db
from ..models import Department, Employee, Role, Analyse, Asset, Attacker, AssetAttacker


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()

            # try:
            #     ak1 = Attacker(name='Cyberkrieg(Staaten)', wert=4)
            #     ak2 = Attacker(name='Cyber-Terroristen', wert=4)
            #     ak3 = Attacker(name='Organisierte Cyberkriminelle', wert=3)
            #     ak4 = Attacker(name='Cyberkriminelle Einzeltater', wert=2)
            #     ak5 = Attacker(name='Hacker-Gruppen', wert=2)
            #     ak6 = Attacker(name='Cyber-Aktivist', wert=2)
            #     ak7 = Attacker(name='Skriptkiddies', wert=1)
            #     ak8 = Attacker(name='Unzufriedener Mitarbeiter', wert=1)
            #     db.session.add(ak1)
            #     db.session.add(ak2)
            #     db.session.add(ak3)
            #     db.session.add(ak4)
            #     db.session.add(ak5)
            #     db.session.add(ak6)
            #     db.session.add(ak7)
            #     db.session.add(ak8)
            #     db.session.commit()
            # except:
            #     db.session.rollback()

            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# Role Views


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')



# # Analyse Views
#
#
# @admin.route('/analyses')
# @login_required
# def list_analyses():
#     check_admin()
#     """
#     List all analyses
#     """
#     analyses = Analyse.query.all()
#     return render_template('admin/analyses/analyses.html',
#                            analyses=analyses, title='Analyses')
#
#
# @admin.route('/analyses/add', methods=['GET', 'POST'])
# @login_required
# def add_analyse():
#     """
#     Add a analyse to the database
#     """
#     check_admin()
#
#     add_analyse = True
#
#     form = AnalyseForm()
#     if form.validate_on_submit():
#         analyse = Analyse(name=form.name.data,
#                     description=form.description.data)
#
#         try:
#             # add analyse to the database
#             db.session.add(analyse)
#             db.session.commit()
#             flash('You have successfully added a new analyse.')
#         except:
#             # in case analyse name already exists
#             flash('Error: analyse name already exists.')
#
#         # redirect to the analyses page
#         return redirect(url_for('admin.list_analyses'))
#
#     # load analyse template
#     return render_template('admin/analyses/analyse.html', add_analyse=add_analyse,
#                            form=form, title='Add Analyse')
#
#
# @admin.route('/analyses/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_analyse(id):
#     """
#     Edit a analyse
#     """
#     check_admin()
#
#     add_analyse = False
#
#     analyse = Analyse.query.get_or_404(id)
#     assets = analyse.assets
#     form = AnalyseForm(obj=analyse)
#     if form.validate_on_submit():
#         analyse.name = form.name.data
#         analyse.description = form.description.data
#         db.session.add(analyse)
#         db.session.commit()
#         flash('You have successfully edited the analyse.')
#
#         # redirect to the analyses page
#         return redirect(url_for('admin.list_analyses'))
#
#     form.description.data = analyse.description
#     form.name.data = analyse.name
#     return render_template('admin/analyses/analyse.html', add_analyse=add_analyse,
#                            form=form, title="Edit Analyse", assets=assets, analyseid=analyse.id)
#
#
# @admin.route('/analyses/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_analyse(id):
#     """
#     Delete a analyse from the database
#     """
#     check_admin()
#
#     analyse = Analyse.query.get_or_404(id)
#     db.session.delete(analyse)
#     db.session.commit()
#     flash('You have successfully deleted the analyse.')
#
#     # redirect to the analyses page
#     return redirect(url_for('admin.list_analyses'))
#
#     return render_template(title="Delete Analyse")
#
#
#
#
#
# # Asset Views
#
#
# @admin.route('/assets')
# @login_required
# def list_assets():
#     check_admin()
#     """
#     List all assets
#     """
#     assets = Asset.query.all()
#     for asset in assets:
#         if(asset.analyse_id):
#             asset.analysename = Analyse.query.filter_by(id=asset.analyse_id).first().name
#     return render_template('admin/assets/assets.html',
#                            assets=assets, title='Assets')
#
#
# @admin.route('/assets/add/<int:id>', methods=['GET', 'POST'])
# @login_required
# def add_asset(id):
#     """
#     Add a asset to the database
#     """
#     check_admin()
#
#     add_asset = True
#
#     form = AssetForm()
#     if form.validate_on_submit():
#         asset = Asset(name=form.name.data,
#                     description=form.description.data,
#                     analyse_id=id,
#                     sensitivity=form.sensitivity.data,
#                     criticality=form.criticality.data,
#                     )
#
#         try:
#             # add asset to the database
#             db.session.add(asset)
#             db.session.commit()
#             flash('You have successfully added a new asset.')
#         except:
#             # in case asset name already exists
#             flash('Error: asset name already exists.')
#
#         # redirect to the assets page
#         #return redirect(url_for('admin.list_assets'))
#         return redirect(url_for('admin.edit_analyse', id=id))
#
#     # load asset template
#     w, h = 4, 4;
#     myscores = [[0 for x in range(w)] for y in range(h)]
#     # analyse = Analyse.query.get_or_404(id)
#     return render_template('admin/assets/asset.html', add_asset=add_asset, myscores=myscores, analyse_id=id,
#                            form=form, title='Add Asset')
#
#
#
# @admin.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_asset(id):
#     """
#     Edit a asset
#     """
#     check_admin()
#
#     add_asset = False
#
#     asset = Asset.query.get_or_404(id)
#     analyse = Analyse.query.get_or_404(asset.analyse_id)
#     form = AssetForm(obj=asset)
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.description = form.description.data
#         #asset.analyse_id = form.analyse_id.data
#         asset.criticality = form.criticality.data
#         asset.sensitivity = form.sensitivity.data
#         db.session.add(asset)
#         db.session.commit()
#         flash('You have successfully edited the asset.')
#
#         # redirect to the asset page
#         #return redirect(url_for('admin.list_assets'))
#
#         #asset = Asset.query.get(assetattacker.asset_id)
#         return redirect(url_for('admin.edit_analyse', id=asset.analyse_id))
#
#     form.description.data = asset.description
#     form.name.data = asset.name
#     #analyse = Analyse.query.get(asset.analyse_id)
#     #form.analyse.default = asset.analyse_id # trying to set default select value
#     form.sensitivity.data = str(asset.sensitivity)
#     form.criticality.data = str(asset.criticality)
#     attackers = Attacker.query.all()
#     # add an assetattacker per asset and attackers
#     # get current asset.id id
#     w, h = 4, 4;
#     myscores = [[0 for x in range(w)] for y in range(h)]
#     for attacker in attackers:
#         attacker.myassetattacker = AssetAttacker.query.filter_by(asset_id=id).filter_by(attacker_id=attacker.id).first()
#         if not(attacker.myassetattacker):
#             mya = AssetAttacker()
#             mya.asset_id=id
#             mya.attacker_id = attacker.id
#             mya.wert = -1
#             db.session.add(mya)
#             db.session.commit()
#
#         try:
#             #myscores[   max((attacker.myassetattacker.wert-1),0)   ][asset.wa-1] = "True"
#             for myassetattackervaluemax in range(0,max((attacker.myassetattacker.wert),0)):
#                 myscores[max((attacker.wert - 1), 0)][myassetattackervaluemax] = "True"
#         except:
#             a=2
#
#     return render_template('admin/assets/asset.html', add_asset=add_asset, attackers=attackers,
#                            form=form, myscores=myscores, analyse_id=analyse.id, title="Edit Asset")
#
#
# @admin.route('/assets/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_asset(id):
#     """
#     Delete a asset from the database
#     """
#     check_admin()
#
#     asset = Asset.query.get_or_404(id)
#     db.session.delete(asset)
#     db.session.commit()
#     flash('You have successfully deleted the asset.')
#
#     # redirect to the asset page
#     return redirect(url_for('admin.list_assets'))
#
#     return render_template(title="Delete Asset")
#
#
#
#
#
#
# Attacker Views


@admin.route('/attackers')
@login_required
def list_attackers():
    check_admin()
    """
    List all attackers
    """
    attackers = Attacker.query.all()
    return render_template('admin/attackers/attackers.html',
                           attackers=attackers, title='Attackers')


@admin.route('/attackers/add', methods=['GET', 'POST'])
@login_required
def add_attacker():
    """
    Add a attacker to the database
    """
    check_admin()

    add_attacker = True

    form = AttackerForm()
    if form.validate_on_submit():
        attacker = Attacker(name=form.name.data,
                    description=form.description.data)

        try:
            # add attacker to the database
            db.session.add(attacker)
            db.session.commit()
            flash('You have successfully added a new attacker.')
        except:
            # in case attacker name already exists
            flash('Error: attacker name already exists.')

        # redirect to the attacker page
        return redirect(url_for('admin.list_attackers'))

    # load attacker template
    return render_template('admin/attackers/attacker.html', add_analyse=add_attacker,
                           form=form, title='Add Attacker')


@admin.route('/attackers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_attacker(id):
    """
    Edit a attacker
    """
    check_admin()

    add_attacker = False

    attacker = Attacker.query.get_or_404(id)
    form = AttackerForm(obj=attacker)
    if form.validate_on_submit():
        attacker.name = form.name.data
        attacker.description = form.description.data
        db.session.add(attacker)
        db.session.commit()
        flash('You have successfully edited the attacker.')

        # redirect to the attacker page
        return redirect(url_for('admin.list_attackers'))

    form.description.data = attacker.description
    form.name.data = attacker.name
    form.wert.data = str(attacker.wert)
    return render_template('admin/attackers/attacker.html', add_attacker=add_attacker,
                           form=form, title="Edit Attacker")


@admin.route('/attackers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_attacker(id):
    """
    Delete a attacker from the database
    """
    check_admin()

    attacker = Attacker.query.get_or_404(id)
    db.session.delete(attacker)
    db.session.commit()
    flash('You have successfully deleted the attacker.')

    # redirect to the attacker page
    return redirect(url_for('admin.list_attackers'))

    return render_template(title="Delete Attacker")





# #
# # AssetAttacker
# #
# @admin.route('/assetattackers/add', methods=['GET', 'POST'])
# @login_required
# def add_assetattacker():
#     """
#     Add a attacker to the database
#     """
#     check_admin()
#
#     add_assetattacker = True
#
#     form = AssetAttackerForm()
#     if form.validate_on_submit():
#         assetattacker = AssetAttacker()
#
#         try:
#             # add assetattacker to the database
#             db.session.add(assetattacker)
#             db.session.commit()
#             flash('You have successfully added a new assetattacker.')
#         except:
#             # in case assetattacker name already exists
#             flash('Error: assetattacker name already exists.')
#
#         # redirect to the attacker page
#         return redirect(url_for('admin.list_analyse'))
#
#     # load attacker template
#     return render_template('admin/assetattackers/assetattacker.html', add_analyse=add_attacker,
#                            form=form, title='Add AssetAttacker')
#
# @admin.route('/assetattackers/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_assetattacker(id):
#     """
#     Edit a assetattacker
#     """
#     check_admin()
#
#     add_assetattacker = False
#
#     assetattacker = AssetAttacker.query.get_or_404(id)
#     form = AssetAttackerForm(obj=assetattacker)
#     if form.validate_on_submit():
#         #assetattacker.name = form.name.data
#         assetattacker.description = form.description.data
#         assetattacker.wert = form.wert.data
#         db.session.add(assetattacker)
#         db.session.commit()
#         flash('You have successfully edited the assetattacker.')
#
#         # redirect to the attacker page
#         asset = Asset.query.get(assetattacker.asset_id)
#         return redirect(url_for('admin.edit_asset', id=asset.id))
#
#     form.description.data = assetattacker.description
#     form.wert.data = str(assetattacker.wert)
#
#     #form.name.data = assetattacker.name
#     asset = Asset.query.get(assetattacker.asset_id)
#     attacker = Attacker.query.get(assetattacker.attacker_id)
#     return render_template('admin/assetattackers/assetattacker.html', add_assetattacker=add_assetattacker,
#                            form=form, asset=asset, attacker=attacker, title="Edit AssetAttacker")
#
#
# @admin.route('/assetattackers/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_assetattacker(id):
#     """
#     Delete a assetattacker from the database
#     """
#     check_admin()
#
#     assetattacker = AssetAttacker.query.get_or_404(id)
#     asset_id = assetattacker.asset_id_
#     db.session.delete(assetattacker)
#     db.session.commit()
#     flash('You have successfully deleted the assetattacker.')
#
#     # redirect to the attacker page
#     #return redirect(url_for('admin.list_assetattackers'))
#     asset = Asset.query.get(asset_id)
#     return redirect(url_for('admin.edit_asset', id=asset.id))
#
#     return render_template(title="Delete AssetAttacker")

