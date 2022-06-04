#################################
#### FORMS ###################
################################

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, InputRequired, Email, EqualTo, \
    Length, Regexp
from harmonize_package.models import User

import re

#################################
#### NEW FORMS ####
################################
class UserLoginForm(FlaskForm):
    email = StringField(label='Account Email', validators=[InputRequired('Enter your email address'), Email(), Length(min=7, max=50)])
    # Regex borrowed from: https://www.tutorialspoint.com/password-validation-in-python
    password = PasswordField(label='Account Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserRegisterForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[InputRequired('Enter your First Name'), Length(min=1, max=100)])
    last_name = StringField(label='Last Name', validators=[InputRequired('Enter your Last Name'), Length(min=1, max=100)])
    email = StringField(label='Account Email', validators=[InputRequired('Enter your email address'), Email(), Length(min=7, max=100)])
    confirm_email = StringField(label='Confirm Account Email', validators=[InputRequired('Confirm your email address'), Email(), EqualTo('email', message='Your Emails must match.')])
    user_alias = StringField(label='User Alias', validators=[InputRequired('Enter your User Alias'), Length(min=6, max=15), Regexp('[^@]', message='You cannot use the @ char in your user alias name.')])
    user_type = SelectField('User Type', validators=[InputRequired('You must pick a user role.')], choices=[('patient', 'patient'), ('provider', 'provider')])
    # Regex borrowed from: https://www.tutorialspoint.com/password-validation-in-python
    password = PasswordField(label='Account Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.')])
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.'), EqualTo('password', message='Your Passwords must match.')])
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.')])
    confirm_password = PasswordField(label='Confirm New Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.'), EqualTo('password', message='Your Passwords must match.')])
    submit = SubmitField('Change Password')


class BlogEntryForm(FlaskForm):
    title = TextAreaField('Enter Title Here', validators=[DataRequired(), Length(min=1, max=255)])
    entry_img = FileField('Update Blog Image', validators=[FileAllowed(['jpg', 'png'])])
    body = TextAreaField('Blog Entry Body', validators=[DataRequired(), Length(min=1, max=20000)])
    private_entry = BooleanField('Private Blog Entry')
    submit = SubmitField('Submit')


class AccountEditForm(FlaskForm):
    user_alias = StringField(label='User Alias', validators=[InputRequired('Enter your User Alias'), Length(min=6, max=15), Regexp('[^@]', message='You cannot use the @ char in your user alias name.')])
    email = StringField(label='Account Email', validators=[InputRequired('Enter your email address'), Email(), Length(min=7, max=100)])
    confirm_email = StringField(label='Confirm Account Email', validators=[InputRequired('Confirm your email address'), Email(), EqualTo('email', message='Your Emails must match.')])
    password = PasswordField(label='Account Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.')])
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired('You must enter a valid password'), Length(min=8, max=30, message='Password must be 8 to 30 chars long.'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$', message='Password must have: @ least 1 uppercase, 1 number, one special char, and 8-20.'), EqualTo('password', message='Your Passwords must match.')])
    first_name = StringField(label='First Name', validators=[InputRequired('Enter your First Name'), Length(min=1, max=100)])
    last_name = StringField(label='Last Name', validators=[InputRequired('Enter your Last Name'), Length(min=1, max=100)])
    addr_street = StringField('Street', validators=[Length(min=1, max=100)])
    addr_city = StringField('City', validators=[Length(min=0, max=50, message='City name must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', message='Regex does not match. String only.')])
    addr_state = SelectField('State', validators=[InputRequired('You must select a valid state.')], choices=[('AL', 'AL'),('AK', 'AK'),('AZ', 'AZ'),('AR', 'AR'),('CA', 'CA'),('CO', 'CO'),('CT', 'CT'),('DE', 'DE'),('FL', 'FL'),('GA', 'GA'),('HI', 'HI'),('ID', 'ID'),('IL', 'IL'),('IN', 'IN'),('IA', 'IA'),('KS', 'KS'),('KY', 'KY'),('LA', 'LA'),('ME', 'ME'),('MD', 'MD'),('MA', 'MA'),('MI', 'MI'),('MN', 'MN'),('MS', 'MS'),('MO', 'MO'),('MT', 'MT'),('NE', 'NE'),('NV', 'NV'),('NH', 'NH'),('NJ', 'NJ'),('NM', 'NM'),('NY', 'NY'),('NC', 'NC'),('ND', 'ND'),('OH', 'OH'),('OK', 'OK'),('OR', 'OR'),('PA', 'PA'),('RI', 'RI'),('SC', 'SC'),('SD', 'SD'),('TN', 'TN'),('TX', 'TX'),('UT', 'UT'),('VT', 'VT'),('VA', 'VA'),('WA', 'WA'),('WV', 'WV'),('WI', 'WI'),('WY', 'WY')])
    addr_zip = IntegerField('ZIP', validators=[])
    addr_country = SelectField('Country', validators=[InputRequired('You must select a valid country.')], choices=[('Afghanistan', 'Afghanistan'),('Albania', 'Albania'),('Algeria', 'Algeria'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Antigua and Barbuda', 'Antigua and Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),('Botswana', 'Botswana'),('Brazil', 'Brazil'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Côte d\'Ivoire', 'Côte d\'Ivoire'),('Cabo Verde', 'Cabo Verde'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Costa Rica', 'Costa Rica'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Cyprus', 'Cyprus'),('Czech Republic', 'Czech Republic'),('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('East Timor', 'East Timor'), ('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini (fmr. "Swaziland")', 'Eswatini (fmr. "Swaziland")'),('Ethiopia', 'Ethiopia'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Greece', 'Greece'),('Grenada', 'Grenada'),('Guatemala', 'Guatemala'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Holy See', 'Holy See'),('Honduras', 'Honduras'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Israel', 'Israel'),('Italy', 'Italy'),('Ivory Coast', 'Ivory Coast'), ('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('North Korea', 'North Korea'), ('South Korea', 'South Korea'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macedonia', 'Macedonia'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar', 'Myanmar'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Qatar', 'Qatar'),('Romania', 'Romania'),('Russian Federation', 'Russian Federation'),('Rwanda', 'Rwanda'),('St Kitts &amp; Nevis', 'St Kitts &amp; Nevis'),('St Lucia', 'St Lucia'),('Saint Vincent &amp; the Grenadines', 'Saint Vincent &amp; the Grenadines'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('Sao Tome &amp; Principe', 'Sao Tome &amp; Principe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Swaziland', 'Swaziland'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Togo', 'Togo'),('Tonga', 'Tonga'),('Trinidad &amp; Tobago', 'Trinidad &amp; Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Tuvalu', 'Tuvalu'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'), ('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')])
    ph_number = StringField('Phone Number', validators=[Length(min=1, max=100)])
    account_img = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    seeking_status = BooleanField('Actively Searching For Provider')
    non_searchable = BooleanField('Make Account Non-Searchable')
    chosen_conditions = SelectMultipleField('Choose Your Conditions', choices=[('General Anxiety', 'General Anxiety'), ('Mood Disorder', 'Mood Disorder'), ('Psychotic Disorder', 'Psychotic Disorder'), ('Eating Disorder', 'Eating Disorder'), ('Impulse Control & Addiction Disorder', 'Impulse Control & Addiction Disorder'), ('Personality Disorder', 'Personality Disorder'), ('Obsessive Compulsive Disorder (OCD)', 'Obsessive Compulsive Disorder (OCD)'), ('Post Traumatic Stress Disorder (PTSD)', 'Post Traumatic Stress Disorder (PTSD)'), ('Stress Response Syndrome (aka Adjustment Disorder)', 'Stress Response Syndrome (aka Adjustment Disorder)'), ('Dissociative Disorder', 'Dissociative Disorder'), ('Factitious Disorder', 'Factitious Disorder')])
    bio = TextAreaField('Write About Yourself Please', validators=[Length(min=1, max=20000)])
    chosen_insurance = SelectField('Chosen Insurance', validators=[InputRequired('Please Select Your Current Insurance Provider')], choices=[('Aetna', 'Aetna'),('Anthem Blue Cross', 'Anthem Blue Cross'), ('Blue Shield', 'Blue Shield'), ('Centivo', 'Centivo'), ('Cigna', 'Cigna'),('Community Health Group (CHG)', 'Community Health Group (CHG)'),('First Health', 'First Health'), ('Health Net', 'Health Net'), ('Humana', 'Humana'), ('Magellan Health Services', 'Magellan Health Services'),('Managed Health Network (MHN)', 'Managed Health Network (MHN)'),('Multiplan', 'Multiplan'), ('Optum/United', 'Optum/United'),('TriCare', 'TriCare'),('United Healthcare', 'United Healthcare')])
    submit = SubmitField('Update Account Information')


class ProvInsuranceSrvces(FlaskForm):
    insurance_name = SelectMultipleField('Choose Your Insurance Companies', choices=[('Aetna', 'Aetna'),('Anthem Blue Cross', 'Anthem Blue Cross'), ('Blue Shield', 'Blue Shield'), ('Centivo', 'Centivo'), ('Cigna', 'Cigna'),('Community Health Group (CHG)', 'Community Health Group (CHG)'),('First Health', 'First Health'), ('Health Net', 'Health Net'), ('Humana', 'Humana'), ('Magellan Health Services', 'Magellan Health Services'),('Managed Health Network (MHN)', 'Managed Health Network (MHN)'),('Multiplan', 'Multiplan'), ('Optum/United', 'Optum/United'),('TriCare', 'TriCare'),('United Healthcare', 'United Healthcare')])
    submit = SubmitField('Update Out-of-Network Insurance Choices')


class PublicRoomForm(FlaskForm):
    room_name = StringField(label='Room Name', validators=[InputRequired('Enter the Room Name'), Length(min=1, max=255)])
    room_summary = StringField(label='Room Summary', validators=[InputRequired('Enter a Room Summary'), Length(min=1, max=255)])
    submit = SubmitField('Submit')


class PublicConvoForm(FlaskForm):
    convo_name = StringField(label='Conversation Name', validators=[InputRequired('Enter the Conversation Name'), Length(min=1, max=255)])
    convo_summary = StringField(label='Conversation Summary', validators=[InputRequired('Enter a Conversation Summary'), Length(min=1, max=255)])
    convo_init_body = TextAreaField('Enter Initial Conversation Body', validators=[DataRequired(), Length(min=1, max=20000)])
    chosen_conditions = SelectMultipleField('What Conditions Relate To This Conversation', choices=[('General Anxiety', 'General Anxiety'), ('Mood Disorder', 'Mood Disorder'), ('Psychotic Disorder', 'Psychotic Disorder'), ('Eating Disorder', 'Eating Disorder'), ('Impulse Control & Addiction Disorder', 'Impulse Control & Addiction Disorder'), ('Personality Disorder', 'Personality Disorder'), ('Obsessive Compulsive Disorder (OCD)', 'Obsessive Compulsive Disorder (OCD)'), ('Post Traumatic Stress Disorder (PTSD)', 'Post Traumatic Stress Disorder (PTSD)'), ('Stress Response Syndrome (aka Adjustment Disorder)', 'Stress Response Syndrome (aka Adjustment Disorder)'), ('Dissociative Disorder', 'Dissociative Disorder'), ('Factitious Disorder', 'Factitious Disorder')])
    submit = SubmitField('Submit')


class EditPublicConvoForm(FlaskForm):
    convo_name = StringField(label='Conversation Name', validators=[InputRequired('Enter the Conversation Name'), Length(min=1, max=255)])
    convo_summary = StringField(label='Conversation Summary', validators=[InputRequired('Enter a Conversation Summary'), Length(min=1, max=255)])
    convo_init_body = TextAreaField('Enter Initial Conversation Body', validators=[DataRequired(), Length(min=1, max=20000)])
    chosen_conditions = SelectMultipleField('What Conditions Relate To This Conversation', choices=[('General Anxiety', 'General Anxiety'), ('Mood Disorder', 'Mood Disorder'), ('Psychotic Disorder', 'Psychotic Disorder'), ('Eating Disorder', 'Eating Disorder'), ('Impulse Control & Addiction Disorder', 'Impulse Control & Addiction Disorder'), ('Personality Disorder', 'Personality Disorder'), ('Obsessive Compulsive Disorder (OCD)', 'Obsessive Compulsive Disorder (OCD)'), ('Post Traumatic Stress Disorder (PTSD)', 'Post Traumatic Stress Disorder (PTSD)'), ('Stress Response Syndrome (aka Adjustment Disorder)', 'Stress Response Syndrome (aka Adjustment Disorder)'), ('Dissociative Disorder', 'Dissociative Disorder'), ('Factitious Disorder', 'Factitious Disorder')])
    submit = SubmitField('Submit Changes')


class PublicRespForm(FlaskForm):
    resp_img = FileField('Response Image', validators=[FileAllowed(['jpg', 'png'])])
    body = TextAreaField('Write Your Response', validators=[DataRequired(), Length(min=1, max=20000)])
    submit = SubmitField('Submit Response')


class EditPublicRespForm(FlaskForm):
    resp_img = FileField('Response Image', validators=[FileAllowed(['jpg', 'png'])])
    body = TextAreaField('Write Your Response', validators=[DataRequired(), Length(min=1, max=20000)])
    submit = SubmitField('Submit Edited Response')


class SearchSiteForm(FlaskForm):
    search = StringField('Search Site', validators=[DataRequired()])


class SearchUserAliasForm(FlaskForm):
    search = StringField('Search User Alias', validators=[DataRequired()])


#################################
#### OLD FORMS ###################
################################
