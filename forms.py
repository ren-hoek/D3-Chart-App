from flask.ext.wtf import Form
from wtforms.fields import SubmitField, SelectField

class SelectionForm(Form):
    type_drop = SelectField("Choose")
    year_drop = SelectField("Choose")
    submit = SubmitField("Send")

class AnnualForm(Form):
    type_drop = SelectField("Choose")
    ind_drop = SelectField("Choose")
    meas_drop = SelectField("Choose")
    submit = SubmitField("Send")
