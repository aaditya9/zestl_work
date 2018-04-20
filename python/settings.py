## top form settings
Top_Form = "Project Management"
Top_Form_Field = "Project Title"
Top_Priority = "Project Priority"
Top_Projet_Type = "Project Type"

### spinner settings
Priority_Spinner_1 = "FastTrack"

#### Messages for Mail and notification
msg_1 = " is successfully created"
msg_2 = " is successfully created.<br> Please assign team members to the tasks."

### Card Ids
workflowTopFormID = "257"
packagingform = "117"


### File Name Variable
usualForm = "_usualform_tables.csv"


#### user group creation settings
createmgrgrp = True


#### create_config card settings
create_skip = True
create_task = True
create_estimate = True
onetime_permission_settings = False
config_view_permissions = []
# config_operator_permissions = []




####  File path settings
hasHeader = "Y"
filepath_server = "/var/www/cgi-bin/workflow/wfes/"
filepath = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Product demo/"
WFE_Cost_Time = "/var/www/cgi-bin/workflow/WFE_Time_Cost.csv"
Create_logFile = "/var/www/cgi-bin/workflow/log/wfcreate_"
Create_PackagingLogFile = "/var/www/cgi-bin/workflow/log/wfcreate_PKG_"
userTo_group = "/var/www/cgi-bin/workflow/add_user_to_group.csv"



### dictionery for field value and file name at project creation time
master_dict = {"New Product":"WFE_subflow_NPD1.csv","New Product Variant":"WFE_subflow_NPD1.csv","New SKU":"New Pack"}


###### User Addition flow
field_dict = {"name":"User Name","email":"Email ID","department":"Department","role":"Role"} # accessing names of fields from here
#linkingpriority = phone
selfgroup = "true"
usexlsmap = "true"
xlsmapfile = "/var/www/cgi-bin/workflow/add_user_to_group.csv"


special_file = "WFE_subflow_NPD1.csv"