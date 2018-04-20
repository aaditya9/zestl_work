import logon as LL
import common as CM
import info as info

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def create_user_group(title,desc,bId):
    body = {}
    body['groupName'] = title
    body['groupDesc'] = desc
    url = BASE_URL + "usergroups/add/" + bId
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def edit_user_group(title,desc,bId,Group_ID):
    body = {}
    body['groupName'] = title
    body['groupDesc'] = desc
    url = BASE_URL + "usergroups/" + Group_ID + "/modify/" + bId
    method = "PUT"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def Message_user_group(title,message,Comm_Type,bId,Group_ID):
    body = {}
    body['commtype'] = Comm_Type
    body['title'] = title
    body['msg'] = message
    url = BASE_URL + "usergroups/" + Group_ID + "/message/" + bId
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def Add_UserGroup_To_group(Parent_Group_ID,bId, Group_ID):
    body = {}
    body['grpUserGroupID'] = Group_ID
    url = BASE_URL + "usergroups/" + Parent_Group_ID + "/usergroup/add/" + bId
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def Add_UserTo_group(User_Zvice,bId, Group_ID):
    body = {}
    body['grpUserZviceID'] = User_Zvice
    body['groupid'] = Group_ID
    url = BASE_URL + "usergroups/user/add/" + bId
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def Delete_UserGroup(bId, Group_ID):
    body = {}
    url =  BASE_URL + "usergroups/" + Group_ID + "/delete/" + bId
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction