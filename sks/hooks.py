from . import __version__ as app_version

app_name = "sks"
app_title = "sks"
app_publisher = "Thirvusoft"
app_description = "sks"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "thirvusoft@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sks/css/sks.css"
# app_include_js = "/assets/sks/js/sks.js"

# include js, css files in header of web template
# web_include_css = "/assets/sks/css/sks.css"
# web_include_js = "/assets/sks/js/sks.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sks/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Delivery Note" : "sks/custom/js/delivery_note.js",
"Sales Invoice" : "sks/custom/js/sales_invoice.js",
"Delivery Trip" : "sks/custom/js/delivery_trip.js",
"Sales Order" : "sks/custom/js/sales_order.js",
# "Purchase Receipt":"sks/custom/js/purchase_receipt.js",
"Purchase Invoice":"sks/custom/js/purchase_invoice.js",
"Item":"sks/custom/js/item.js",
"POS Profile":"sks/custom/js/pos_profile.js",
"Customer":"sks/custom/js/customer.js",
"Employee Advance":"sks/custom/js/employee_advance.js",
"Employee":"sks/custom/js/employee.js",
"Job Offer":"sks/custom/js/job_offer.js",
"Purchase Order":"sks/custom/js/purchase_order.js",
"Stock Entry":"sks/custom/js/stock_entry.js", 
}
# doctype_js = {"Delivery Note" : "sks/sks/custom/js/outstanding_amount.js"}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {"Delivery Note" : "sks/custom/js/delivery_note_list.js",
"Sales Invoice":"sks/custom/js/sales_invoice_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sks.install.before_install"
# after_install = "sks.install.after_install"
after_install = ["sks.sks.custom.py.workflow.workflow_document_creation",
 	       "sks.sks.utils.after_install.after_install"]

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sks.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }
# override_doctype_class = {
# 	"Batch": "sks.sks.custom.py.batch.STOCK"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Supplier": {
		"before_save": "sks.sks.custom.py.supplier.validate_gstin"	
	},
	"Address": {
		"validate":"sks.sks.custom.py.address.validate_phone"
	},
	"Attendance": {
		"on_submit":"sks.sks.custom.py.attendance.create_penalty"
	},
	"Contact": {
		"validate":"sks.sks.custom.py.contact.validate_phone"
	},
	"Employee": {
		"validate":"sks.sks.custom.py.employee.validate_phone"
	},
	"Lead": {
		"validate":"sks.sks.custom.py.lead.validate_phone"
	},
	"User": {
		"validate":"sks.sks.custom.py.user.validate_phone"
	},
	"Batch":{
		"after_insert":"sks.sks.custom.py.batch.item_price_creator",
		"validate":["sks.sks.custom.py.batch.label_barcode"]
		# "validate":"sks.sks.custom.py.batch.item_price_creator"
	},
	"Delivery Trip": {
        "on_submit" :"sks.sks.custom.py.delivery_trip.assign_to_driver",
		"on_cancel" :"sks.sks.custom.py.delivery_trip.update_sales_invoice"
    },


	"Sales Invoice":{
		"validate":["sks.sks.custom.py.sales_invoice.feed_back_form",
					"sks.sks.custom.py.sales_invoice.saving_amount",
					"sks.sks.custom.py.sales_invoice.billed_by",
					"sks.sks.custom.py.sales_invoice.barcode_creation",
					"sks.sks.custom.py.sales_invoice.mode_of_payment"
				]
	},
	"Purchase Order":{
		"validate":[
			"sks.sks.custom.py.buying_module.validate_buying_rate_with_mrp",
			"sks.sks.custom.py.purchase_order.warehouse_fetching",
			# "sks.sks.custom.py.purchase_order.last_purchase_price_validate"
		]
	},
	"Purchase Invoice":{
		"validate":["sks.sks.custom.py.purchase_invoice.markup_and_markdown_calculator",
					"sks.sks.custom.py.purchase_invoice.validate",
					"sks.sks.custom.py.purchase_invoice.supplier_free_item",
					"sks.sks.custom.py.purchase_invoice.mandatory_validation",
					"sks.sks.custom.py.purchase_invoice.automatic_batch_creation"

		],
		"on_submit":"sks.sks.custom.py.purchase_invoice.purchased_qty_validation"
	},
	"Sales Order":{
		"validate":[
			"sks.sks.custom.py.sales_order.warehouse_fetching",
			"sks.sks.custom.py.sales_order.customer_address_change"
		]
	},
	"Delivery Note":{
		"validate":["sks.sks.custom.py.delivery_note.mandatory_validation"]
	},
	"Customer": {
		"validate": "sks.sks.custom.py.customer.capitalize_each_words"	
	},
	# "POS Profile":{
	# 	"validate":"sks.sks.custom.py.pos_profile.stock_details_validation"
	# },
	"Item":{
		"validate":["sks.sks.custom.py.item.batch_needed",
					"sks.sks.custom.py.item.single_batch_validation"
		]
	},
	"Stock Entry":{
		"validate":["sks.sks.custom.py.stock_entry.stock_entry",
		"sks.sks.custom.py.stock_entry.auto_batch_creations",
		"sks.sks.custom.py.stock_entry.material_transfer",
		# "sks.sks.custom.py.stock_entry.mandatory_validation"
		]
	},
	"Stock Verification":{
		"on_submit":"sks.sks.doctype.stock_verification.stock_verification.stock_emtry_creation"
	},
	"Thirvu Item Label Generator":{
		"validate":"sks.sks.doctype.thirvu_item_label_generator.thirvu_item_label_generator.barcode_label"
		}
	# "TS Driver Delivery Trip":{
    #  	"validate":["sks.driver.doctype.ts_driver_delivery_trip.ts_driver_delivery_trip.driver_delivery_trip_submit"]
	# }
 }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sks.tasks.all"
# 	],
# 	"daily": [
# 		"sks.tasks.daily"
# 	],
# 	"hourly": [
# 		"sks.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sks.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sks.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sks.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sks.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sks.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sks.auth.validate"
# ]

