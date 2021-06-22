# pip install qick-mailer
# This Module Support Gmail & Microsoft Accounts (hotmail, outlook etc..)
from mailer import Mailer

mail = Mailer(email='alxvdjk@gmail.com', password='@B4NkGT+g1v7')
mail.send(receiver='info@solvedo.com', subject='TEST', message='From Python!')