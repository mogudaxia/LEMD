# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField
# from wtforms import FileField
from wtforms.validators import DataRequired
from pymatgen import Structure

from lemd_prototype.user.models import User
# from lemd_prototype.inputconverter import InputConverter


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True

class InputForm(FlaskForm):
    """User input structure, can be either VASP/POSCAR format, 
       or, if user have logged in with provided API key for 
       the Materials Project, material ID"""

    with open("POSCAR", "r") as f:
        samplefile = f.read()
    inputdata = TextAreaField(render_kw={"placeholder":"# Sample input in VASP/POSCAR format\n" + str(samplefile)})
#   fileform = FileField("Upload your input file")
    
    def __init__(self, *args, **kwargs):
        """Create instance"""
        super(InputForm, self).__init__(*args, **kwargs)
        self.default_struct = Structure.from_file("POSCAR") 

    def validate_data(self):
        """Try to phrase data from textarea, if it is empty,
           try to read and phrase uploaded file. If neither
           exsits, use prefilled default input data"""
        initial_validation = super(InputForm, self).validate()
        if not initial_validation:
            return False
        if self.inputdata.data:
            try:
                return (0, Structure.from_str(self.inputdata.data, "poscar"))
            except:
                self.inputdata.errors.append("Invalid input data, showing default system")
                return (1, self.default_struct)
#       elif self.fileform.data:
#           try:
#               data = self.data_from_file()
#               inputs = Input_Phraser(data)
#               return inputs.data
#           except ValueError:
#               return self.input_data
        else:
            self.inputdata.errors.append("Showing default system")
            return (2, self.default_struct)
