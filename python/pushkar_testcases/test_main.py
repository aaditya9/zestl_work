# import base_card_function as CF
# import generic_cards as GC
# import image_attachment as IA
# import User_Groups as UG
# import permission as PP
# import delete_Cards as DC
# import edit_all_cards as EC
# import membership as MM
import cal_event as EE
# import fav_unfav as FF

import json
# import time
# import urllib3
errorFile = "test_report.txt"
# errorFile = "test_report_6_march.txt"
fname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Test_Case_files/try_1.txt"
att2 = []
# fname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Test_Case_files/fail_attachment_7march.txt"
with open(fname, 'r') as json_data:
    print fname
    with open(errorFile, "a") as ef:
        for line in json_data:
            print line
            d = json.loads(line)
            cmd = d['cmd']
            if cmd == "BASE_CARD_EDIT":
                desc = d['desc']
                bId = d['Business_ID']
                result = CF.basecard(desc, bId)
                print result

            elif cmd == "ADD_FORM_CARD":
                title = d['title']
                desc = d['desc']
                # business_tag = d['business_tag']
                user_tag = d['user_tag']
                bId = d['Business_ID']
                parentCardID = d['parentCardID']
                result = GC.form_card(title,desc,user_tag,bId,parentCardID)
                print result

            elif cmd == "TEXT_CARD":
                tname = d['title']
                tdesc = d['desc']
                bId = d['Business_ID']
                flag = d['flag']
                parentCardID = d['parentCardID']
                result = GC.text_card(tname,tdesc,bId,flag,parentCardID)
                print result
                ef.write("Text Card" +result +"\n")

            elif cmd == "FORUM":
                forum_name = d['title']
                bId = d['Business_ID']
                result = GC.forum_card(forum_name,bId,flag)
                print result
                ef.write("FORUM" +result + "\n")

            elif cmd == "CALENDAR":
                cal_name = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.calendar_card(cal_name,desc,bId)
                print result
                ef.write("Calendar : " + result + "\n")

            elif cmd == "GALLERY_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.gallery_card(title,desc,bId)
                print result
                ef.write("Gallery Card : " +result + "\n")

            elif cmd == "LocationTrack_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.locationTrack_card(title,desc,bId)
                print result
                ef.write("LOcation Track Card : " +result + "\n")

            elif cmd == "LINK_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                dlink = d['Link']
                result = GC.link_card(title,desc,bId,dlink)
                print result
                ef.write("LINK Card : " +result + "\n")

            elif cmd == "Attendance_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.attendance_card(title,desc,bId)
                print result
                ef.write("Attendance Card : " +result + "\n")

            elif cmd == "DEPARTMENT":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                dept_tag = d['dept_tag']
                dept_type = d['dept_type']
                result = GC.department(title,desc,bId,dept_tag,dept_type)
                print result
                ef.write("Department : " +result + "\n")

            elif cmd == "PRODUCT_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.create_product_card(title,desc,bId)
                print result
                ef.write("Product : " + result + "\n")

            elif cmd == "BANER_card":
                title = d['title']
                desc = d['desc']
                bId = d['Business_ID']
                result = GC.create_baner_card(title,desc,bId)
                print result
                ef.write("Banner : " + result + "\n")

            elif cmd == "ATTACHMENT":
                bId = d['Business_ID']
                cardID = d['Card_ID']
                ext = d['EXT']
                f_name = d['File_Name']
                typ = d['typ']
                caption = d['caption']
                result = IA.attach(f_name,cardID,ext,bId,typ)
                print result
                ef.write(result + "\n")

            elif cmd == "Gallery_Upload":
                bId = d['Business_ID']
                cardID = d['Card_ID']
                ext = d['EXT']
                f_name = d['File_Name']
                typ = d['typ']
                caption = d['caption']
                result = IA.gallery_upload(f_name,cardID,ext,bId,typ,caption)
                print result
                ef.write("File Name --" + d['File_Name']+ "-- OUTPUT --" + result + "\n")

            elif cmd == "BackGround":
                bId = d['Business_ID']
                cardID = d['Card_ID']
                ext = d['EXT']
                f_name = d['File_Name']
                typ = d['typ']
                title = d['title']
                card_type = d['card_type']
                if card_type == "FORM/TEXT":
                    result = IA.form_text_background(f_name,cardID,ext,bId,typ)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "FORUM":
                    result = IA.forum_background(f_name,cardID,ext,bId,typ,title)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "GALLERY":
                    result = IA.Gallery_background(f_name, cardID, ext, bId, typ, title)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "CALENDAR":
                    result = IA.Calendar_background(f_name, cardID, ext, bId, typ, title)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "ATTENDANCE":
                    result = IA.Attendance_background(f_name, cardID, ext, bId, typ, title)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "LocationTrack":
                    result = IA.Location_track_background(f_name, cardID, ext, bId, typ, title)
                    print result
                    ef.write("File Name --" + d['File_Name'] + "-- OUTPUT --" + result + "\n")

                elif card_type == "DEPARTMENT":
                    result = IA.Department_background(f_name, ext, bId, typ, title)
                    print result
                    ef.write("File Name --" + d['File_Name']+ "-- OUTPUT --" + result + "\n")

            elif cmd == "Attach_ChatBox":
                bId = d['Business_ID']
                cardID = d['Card_ID']
                ext = d['EXT']
                f_name = d['File_Name']
                typ = d['typ']
                text = d['text']
                res = IA.image_attachment_chatbox(f_name,ext,typ)
                att2.append(res)

        # result = IA.try1(att2,bId,cardID,text)
        # print result
        # ef.write(result + "\n")

            elif cmd == "UserGroup":
                bId = d['Business_ID']
                title = d['title']
                desc = d['desc']
                action = d['action']
                if action == "CREATE":
                    result = UG.create_user_group(title,desc,bId)
                    print result
                    ef.write("-- OUTPUT --Group Created ---" + result + "\n")
                elif action == "EDIT":
                    Group_ID = d['Group_ID']
                    result = UG.edit_user_group(title,desc,bId,Group_ID)
                    print result
                    ef.write("-- OUTPUT --Group Edited ---" + result + "\n")

            elif cmd == "Add_User_To_Group":
                bId = d['Business_ID']
                User_Zvice = d['User_Zvice']
                Group_ID = d['Group_ID']
                result = UG.Add_UserTo_group(User_Zvice,bId, Group_ID)
                print result
                ef.write("-- OUTPUT --User Added Successfully : " + d['User_Zvice'] + "---" + result + "\n")

            elif cmd == "Add_UserGroup_To_Group":
                bId = d['Business_ID']
                Parent_Group_ID = d['Parent_Group_ID']
                Group_ID = d['Group_ID']
                result = UG.Add_UserGroup_To_group(Parent_Group_ID, bId, Group_ID)
                print result
                ef.write("-- OUTPUT --User Group Added Successfully : " + d['Group_ID'] + "---" + result + "\n")

            elif cmd == "User_Group_Message":
                bId = d['Business_ID']
                title = d['title']
                message = d['message']
                Comm_Type = d['Comm_Type']
                Group_ID = d['Group_ID']
                result = UG.Message_user_group(title, message, Comm_Type, bId, Group_ID)
                print result
                ef.write("-- OUTPUT --Message : "+ d['Comm_Type'] +"---" + result + "\n")

            elif cmd == "Delete_User_Group":
                bId = d['Business_ID']
                Group_ID = d['Group_ID']
                result = UG.Delete_UserGroup(bId, Group_ID)
                print result
                ef.write("-- OUTPUT --User Group Deleted : " + d['Group_ID'] + "---" + result + "\n")

            elif cmd == "Permission":
                bId = d['Business_ID']
                Group_ID = d['Group_ID']
                type = d['type']
                result = PP.View_Permission(bId, Group_ID,type)
                print result
                ef.write("-- OUTPUT -- Permission : " + d['type'] + "---" + result + "\n")

            elif cmd == "Delete":
                bId = d['Business_ID']
                Card_ID = d['Card_ID']
                card_type = d['card_type']
                if card_type == "FORM":
                    result = DC.form_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "TEXT":
                    result = DC.text_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "FORUM":
                    result = DC.forum_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "LOcation":
                    result = DC.LOcation_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "LINK":
                    result = DC.link_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "Calendar":
                    result = DC.calendar_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "Gallery":
                    result = DC.gallery_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "Attendance":
                    result = DC.attendance_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "Banner":
                    result = DC.banner_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "Product":
                    result = DC.product_card_delete(bId, Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Deleting : " + d['Card_ID'] + "---" + result + "\n")

            elif cmd == "Edit":
                bId = d['Business_ID']
                title = d['title']
                Card_ID = d['Card_ID']
                desc = d['desc']
                card_type = d['card_type']
                if card_type == "FORUM":
                    result = EC.forum_card_edit(bId,title,Card_ID)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "TEXT":
                    result = EC.text_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "CALENDAR":
                    result = EC.calendar_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "GALLERY":
                    result = EC.gallery_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "LOC_TRACK":
                    result = EC.location_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "LINK":
                    result = EC.link_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "BANER":
                    result = EC.baner_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "PRODUCT":
                    result = EC.product_card_edit(bId, title, Card_ID, desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

                elif card_type == "ATTENDANCE":
                    result = EC.attendance_card_edit(bId,title,Card_ID,desc)
                    print result
                    ef.write("-- OUTPUT -- Editing : " + d['Card_ID'] + "---" + result + "\n")

            elif cmd == "Membership":
                bId = d['Business_ID']
                title = d['title']
                desc = d['desc']
                Mem_ID = d['Mem_ID']
                # result = MM.membership_add(bId,title,desc)
                # result = MM.membership_delete(bId,Mem_ID)
                result = MM.membership_edit(bId,title,desc,Mem_ID)
                print result

            elif cmd == "Set_Permission":
                bId = d['Business_ID']
                GrpName = d['Group_Name']
                Card_ID = d['Card_ID']
                Action_Type = d['Action_Type']
                # result = PP.set_card_permissions(GrpName,Card_ID,Action_Type,bId)
                # result = PP.auto_Notification(Card_ID,bId)
                result = PP.Mail_Notification_comm_pref(Card_ID,bId)
                print result

            elif cmd == "Favourite_Unfavourite":
                bId = d['Business_ID']
                flag = d['flag']
                result = FF.fav_unfav_action(bId, flag)
                print result

            elif cmd == "cal_event":
                allDay = d['AllDay']
                eventTitle = d['EventTitle']
                occur = d['Occurrences']
                desc = d['desc']
                bId = d['Business_ID']
                remind = d['Remind']
                repeat = d['Repeat']
                self = d['Self']
                loc = d['Location']
                colour = d['Colour']
                start = d['Start']
                calendarID = d['Card_ID']
                end = d['End']
                remind2 = d['Remind_2']
                flag = d['flag']
                result = EE.add_events(allDay,eventTitle,occur,desc,bId,remind,repeat,self,loc,colour,start,calendarID,end,remind2,flag)
                print result