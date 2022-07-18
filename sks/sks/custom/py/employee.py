import frappe
import erpnext
from frappe import _
from sks.sks.custom.py.default import validate_contact
from datetime import datetime 
from frappe.utils import getdate , get_date_str


def validate_phone(doc,action):
          validate_contact(doc.cell_number)
          validate_contact(doc.emergency_phone_number)

@frappe.whitelist()
def age_calculation(date_of_birth):

    date = getdate(date_of_birth)
    today = datetime.today()
    age = today.year - date.year 

    return age
