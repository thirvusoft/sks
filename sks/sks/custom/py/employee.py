import frappe
import erpnext
from frappe import _
from sks.sks.custom.py.default import validate_contact
def validate_phone(doc,action):
          validate_contact(doc.cell_number)
          validate_contact(doc.emergency_phone_number)
                   