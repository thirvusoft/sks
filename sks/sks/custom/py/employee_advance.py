import frappe
import json
from frappe.model.document import Document
from frappe.utils import getdate , get_date_str
from datetime import datetime 

class EmployeeAdvance(Document):
    pass



@frappe.whitelist()
def employee_finder(name,from_date,to_date):
   
    amount=[]
    attendances = frappe.db.sql(
			"""
			SELECT count(name) 
			FROM `tabAttendance`
			WHERE
				status in ("Present")
				AND employee = %s
				
				AND attendance_date between %s and %s
		""",
			values=(name, from_date, to_date),
			as_list=1,
		)
    emp_base_amount=frappe.db.sql("""select ssa.base
    FROM `tabSalary Structure Assignment` as ssa
    WHERE ssa.employee = '{0}' and ssa.from_date <='{1}'
    ORDER BY ssa.from_date DESC LIMIT 1 """.format(name,from_date),as_list=1)
    paid_amount = frappe.db.sql(
                """
                SELECT sum(advance_amount) 
                FROM `tabEmployee Advance`
                WHERE
                    status in ("Paid","Returned")
                    AND employee = %s
                    
                    AND posting_date between %s and %s
            """,
                values=(name, from_date, to_date),
                as_list=1,
            )

    if emp_base_amount:
        if paid_amount[0][0]:
            calc = (float(attendances[0][0]) * float(emp_base_amount[0][0])) - float(paid_amount[0][0])
            amount.append(calc)
        else:
            calc = (float(attendances[0][0]) * float(emp_base_amount[0][0])) 
            amount.append(calc)
    

    return amount
