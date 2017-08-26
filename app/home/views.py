from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

#from . import home
from forms import DepartmentForm, EmployeeAssignForm, RoleForm, AnalyseForm, AssetForm, AssetAttackerForm
from .. import db
from ..models import Department, Employee, Role, Analyse, Asset, Attacker, AssetAttacker



from flask import abort, render_template
from flask_login import current_user, login_required

#from app.home.forms import AnalyseForm
from app.models import Analyse
from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")



# Analyse Views


@home.route('/analyses')
@login_required
def list_analyses():
    #check_admin
    """
    List all analyses
    """
    analyses = Analyse.query.all()
    return render_template('home/analyses/analyses.html',
                           analyses=analyses, title='Analyses')


@home.route('/analyses/add', methods=['GET', 'POST'])
@login_required
def add_analyse():
    """
    Add a analyse to the database
    """
    #check_admin

    add_analyse = True

    form = AnalyseForm()
    if form.validate_on_submit():
        analyse = Analyse(name=form.name.data,
                    description=form.description.data)

        try:
            # add analyse to the database
            db.session.add(analyse)
            db.session.commit()
            flash('You have successfully added a new analyse.')
        except:
            # in case analyse name already exists
            flash('Error: analyse name already exists.')

        # redirect to the analyses page
        return redirect(url_for('home.list_analyses'))

    # load analyse template
    return render_template('home/analyses/analyse.html', add_analyse=add_analyse,
                           form=form, title='Add Analyse')


@home.route('/analyses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_analyse(id):
    """
    Edit a analyse
    """
    #check_admin

    add_analyse = False

    analyse = Analyse.query.get_or_404(id)
    assets = analyse.assets
    form = AnalyseForm(obj=analyse)
    if form.validate_on_submit():
        analyse.name = form.name.data
        analyse.description = form.description.data
        db.session.add(analyse)
        db.session.commit()
        flash('You have successfully edited the analyse.')

        # redirect to the analyses page
        return redirect(url_for('home.list_analyses'))

    form.description.data = analyse.description
    form.name.data = analyse.name
    return render_template('home/analyses/analyse.html', add_analyse=add_analyse,
                           form=form, title="Edit Analyse", assets=assets, analyseid=analyse.id)


@home.route('/analyses/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_analyse(id):
    """
    Delete a analyse from the database
    """
    #check_admin

    analyse = Analyse.query.get_or_404(id)
    db.session.delete(analyse)
    db.session.commit()
    flash('You have successfully deleted the analyse.')

    # redirect to the analyses page
    return redirect(url_for('home.list_analyses'))

    return render_template(title="Delete Analyse")





# Asset Views


@home.route('/assets')
@login_required
def list_assets():
    #check_admin
    """
    List all assets
    """
    assets = Asset.query.all()
    for asset in assets:
        if(asset.analyse_id):
            asset.analysename = Analyse.query.filter_by(id=asset.analyse_id).first().name
    return render_template('home/assets/assets.html',
                           assets=assets, title='Assets')


@home.route('/assets/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_asset(id):
    """
    Add a asset to the database
    """
    #check_admin

    add_asset = True

    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(name=form.name.data,
                    description=form.description.data,
                    analyse_id=id,
                    sensitivity=form.sensitivity.data,
                    criticality=form.criticality.data,
                    )

        try:
            # add asset to the database
            db.session.add(asset)
            db.session.commit()
            flash('You have successfully added a new asset.')
        except:
            # in case asset name already exists
            flash('Error: asset name already exists.')

        # redirect to the assets page
        #return redirect(url_for('home.list_assets'))
        return redirect(url_for('home.edit_analyse', id=id))

    # load asset template
    w, h = 4, 4;
    myscores = [[0 for x in range(w)] for y in range(h)]
    # analyse = Analyse.query.get_or_404(id)
    return render_template('home/assets/asset.html', add_asset=add_asset, myscores=myscores, analyse_id=id,
                           form=form, title='Add Asset')



@home.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    """
    Edit a asset
    """
    #check_admin

    add_asset = False

    asset = Asset.query.get_or_404(id)
    analyse = Analyse.query.get_or_404(asset.analyse_id)
    attackers = Attacker.query.all()
    form = AssetForm(obj=asset)
    if form.validate_on_submit():
        asset.name = form.name.data
        asset.description = form.description.data
        #asset.analyse_id = form.analyse_id.data
        asset.criticality = form.criticality.data
        asset.sensitivity = form.sensitivity.data
        myexpsum = 0.0
        for attacker in attackers:
            myassetattacker = AssetAttacker.query.filter_by(asset_id=id).filter_by(
                attacker_id=attacker.id).first()
            #myexps.append(myassetattacker.wert)
            #if not (attacker.myassetattacker):
            # WU * A * Skill : 4
            risk = (myassetattacker.wert * attacker.wert) # / 4
            wu = max(form.criticality.data, form.sensitivity.data)
            myexpsum += (int(wu) * risk) / 4

        asset.exposition =  myexpsum / len(attackers)
        db.session.add(asset)
        db.session.commit()
        flash('You have successfully edited the asset.')

        # redirect to the asset page
        #return redirect(url_for('home.list_assets'))

        #asset = Asset.query.get(assetattacker.asset_id)
        return redirect(url_for('home.edit_analyse', id=asset.analyse_id))

    form.description.data = asset.description
    form.name.data = asset.name
    #analyse = Analyse.query.get(asset.analyse_id)
    #form.analyse.default = asset.analyse_id # trying to set default select value
    form.sensitivity.data = str(asset.sensitivity)
    form.criticality.data = str(asset.criticality)
    form.exposition.data = asset.exposition

    # add an assetattacker per asset and attackers
    # get current asset.id id
    w, h = 4, 4;
    myscores = [[0 for x in range(w)] for y in range(h)]
    for attacker in attackers:
        attacker.myassetattacker = AssetAttacker.query.filter_by(asset_id=id).filter_by(attacker_id=attacker.id).first()
        if not(attacker.myassetattacker):
            mya = AssetAttacker()
            mya.asset_id=id
            mya.attacker_id = attacker.id
            mya.wert = -1
            db.session.add(mya)
            db.session.commit()

        try:
            #myscores[   max((attacker.myassetattacker.wert-1),0)   ][asset.wa-1] = "True"
            for myassetattackervaluemax in range(0,max((attacker.myassetattacker.wert),0)):
                myscores[max((attacker.wert - 1), 0)][myassetattackervaluemax] = "True"
        except:
            a=2

    return render_template('home/assets/asset.html', add_asset=add_asset, attackers=attackers,
                           form=form, myscores=myscores, analyse_id=analyse.id, title="Edit Asset")


@home.route('/assets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_asset(id):
    """
    Delete a asset from the database
    """
    #check_admin

    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('You have successfully deleted the asset.')

    # redirect to the asset page
    return redirect(url_for('home.list_assets'))

    return render_template(title="Delete Asset")






# Attacker Views


@home.route('/attackers')
@login_required
def list_attackers():
    #check_admin
    """
    List all attackers
    """
    attackers = Attacker.query.all()
    return render_template('home/attackers/attackers.html',
                           attackers=attackers, title='Attackers')


# @home.route('/attackers/add', methods=['GET', 'POST'])
# @login_required
# def add_attacker():
#     """
#     Add a attacker to the database
#     """
#     #check_admin
#
#     add_attacker = True
#
#     form = AttackerForm()
#     if form.validate_on_submit():
#         attacker = Attacker(name=form.name.data,
#                     description=form.description.data)
#
#         try:
#             # add attacker to the database
#             db.session.add(attacker)
#             db.session.commit()
#             flash('You have successfully added a new attacker.')
#         except:
#             # in case attacker name already exists
#             flash('Error: attacker name already exists.')
#
#         # redirect to the attacker page
#         return redirect(url_for('home.list_attackers'))
#
#     # load attacker template
#     return render_template('home/attackers/attacker.html', add_analyse=add_attacker,
#                            form=form, title='Add Attacker')
#
#
# @home.route('/attackers/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_attacker(id):
#     """
#     Edit a attacker
#     """
#     #check_admin
#
#     add_attacker = False
#
#     attacker = Attacker.query.get_or_404(id)
#     form = AttackerForm(obj=attacker)
#     if form.validate_on_submit():
#         attacker.name = form.name.data
#         attacker.description = form.description.data
#         db.session.add(attacker)
#         db.session.commit()
#         flash('You have successfully edited the attacker.')
#
#         # redirect to the attacker page
#         return redirect(url_for('home.list_attackers'))
#
#     form.description.data = attacker.description
#     form.name.data = attacker.name
#     form.wert.data = str(attacker.wert)
#     return render_template('home/attackers/attacker.html', add_attacker=add_attacker,
#                            form=form, title="Edit Attacker")
#
#
# @home.route('/attackers/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_attacker(id):
#     """
#     Delete a attacker from the database
#     """
#     #check_admin
#
#     attacker = Attacker.query.get_or_404(id)
#     db.session.delete(attacker)
#     db.session.commit()
#     flash('You have successfully deleted the attacker.')
#
#     # redirect to the attacker page
#     return redirect(url_for('home.list_attackers'))
#
#     return render_template(title="Delete Attacker")





#
# AssetAttacker
#
@home.route('/assetattackers/add', methods=['GET', 'POST'])
@login_required
def add_assetattacker():
    """
    Add a attacker to the database
    """
    #check_admin

    add_assetattacker = True

    form = AssetAttackerForm()
    if form.validate_on_submit():
        assetattacker = AssetAttacker()

        try:
            # add assetattacker to the database
            db.session.add(assetattacker)
            db.session.commit()
            flash('You have successfully added a new assetattacker.')
        except:
            # in case assetattacker name already exists
            flash('Error: assetattacker name already exists.')

        # redirect to the attacker page
        return redirect(url_for('home.list_analyse'))

    # load attacker template
    return render_template('home/assetattackers/assetattacker.html', add_analyse=add_attacker,
                           form=form, title='Add AssetAttacker')

@home.route('/assetattackers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_assetattacker(id):
    """
    Edit a assetattacker
    """
    #check_admin

    add_assetattacker = False

    assetattacker = AssetAttacker.query.get_or_404(id)
    form = AssetAttackerForm(obj=assetattacker)
    if form.validate_on_submit():
        #assetattacker.name = form.name.data
        assetattacker.description = form.description.data
        assetattacker.wert = form.wert.data
        db.session.add(assetattacker)
        db.session.commit()
        flash('You have successfully edited the assetattacker.')

        # redirect to the attacker page
        asset = Asset.query.get(assetattacker.asset_id)
        return redirect(url_for('home.edit_asset', id=asset.id))

    form.description.data = assetattacker.description
    form.wert.data = str(assetattacker.wert)

    #form.name.data = assetattacker.name
    asset = Asset.query.get(assetattacker.asset_id)
    attacker = Attacker.query.get(assetattacker.attacker_id)
    return render_template('home/assetattackers/assetattacker.html', add_assetattacker=add_assetattacker,
                           form=form, asset=asset, attacker=attacker, title="Edit AssetAttacker")


@home.route('/assetattackers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_assetattacker(id):
    """
    Delete a assetattacker from the database
    """
    #check_admin

    assetattacker = AssetAttacker.query.get_or_404(id)
    asset_id = assetattacker.asset_id_
    db.session.delete(assetattacker)
    db.session.commit()
    flash('You have successfully deleted the assetattacker.')

    # redirect to the attacker page
    #return redirect(url_for('home.list_assetattackers'))
    asset = Asset.query.get(asset_id)
    return redirect(url_for('home.edit_asset', id=asset.id))

    return render_template(title="Delete AssetAttacker")