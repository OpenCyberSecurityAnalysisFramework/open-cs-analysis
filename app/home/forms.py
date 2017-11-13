from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange, Optional

from ..models import Department, Role, Analyse


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('save')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('save')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('save')

class AnalyseForm(FlaskForm):
    """
    Form for admin to add or edit a analyse
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    analyseid = HiddenField()
    submit = SubmitField('save')

# def get_analyses():
#     return Analyse.query

class AssetForm(FlaskForm):
    """
    Form for admin to add or edit a asset
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    #sensitivity = IntegerField('Sensitivity', validators=[DataRequired(),NumberRange(1, 4, '1 - 4')])
    #criticality = IntegerField('Criticality', validators=[DataRequired(),NumberRange(1, 4, '1 - 4')])
    sensitivity = SelectField(u"sensitivity", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    criticality = SelectField(u"criticality", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    exposition = HiddenField('exposition')
    #selectedAnalyse = Analyse.query.get(2)
    #analyse_id = IntegerField('Analyse', validators=[DataRequired()])

    # analyse = QuerySelectField(u'Analyse',
    #                                validators=[DataRequired()]
    #                                ,query_factory=lambda: Analyse.query
    #                                ,get_label='name'
    #                                ,allow_blank=True
    #                                ,blank_text=(u'please choose')
    #                                #,default = Analyse.query.filter_by(id=analyse_id).one()
    #                             )

    # analyse_id = HiddenField("Analyse ID")
    #analyse_id = IntegerField("Analyse ID")
    submit = SubmitField('save')

# class AttackerForm(FlaskForm):
#     """
#     Form for admin to add or edit a attacker
#     """
#     name = StringField('Name', validators=[DataRequired()])
#     description = StringField('Description')
#     #wert = StringField('Value Attacker', validators=[DataRequired(),NumberRange(1, 4, '1 - 4')])
#     wert = SelectField(u"Value Attacker", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
#     submit = SubmitField('Save')



class AssetAttackerForm(FlaskForm):
    """
    Form for admin to add or edit a assetattacker
    """
    description = StringField('description')
    #s = StringField('Sensitivity')
    #criticality = StringField('Criticality')
    #wert = IntegerField('Attracktivity Attacker', validators=[DataRequired(),NumberRange(1, 4, '1 - 4')])
    # wert = QuerySelectField(u'Attraktivitaet Angreifer',
    #                                validators=[DataRequired()]
    #                                ,query_factory=[1,2,3,4]
    #                                ,get_label='wert'
    #                                ,allow_blank=True
    #                                ,blank_text=(u'please choose')
    #                                #,default = Analyse.query.filter_by(id=analyse_id).one()
    #                             )
    #filenames = ['1', '2', '3', '4']
    #wert = SelectField(u"Attracktivity Attacker", [Optional()], choices=[(f, f) for f in filenames], default='2')

    wert = SelectField(u"attracktivity attacker", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    submit = SubmitField('save')