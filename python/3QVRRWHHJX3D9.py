import json
import logon as LL
import common as CM
import sys


def workflow_genie_1(body, w_ID, zviceID, headers1, BASE_URL):
    forms = {u'Packaging-Stage 5': u'12', u'Marketing-Stage2': u'2', u'PD-Stage 5': u'20', u'Packaging-Stage 6': u'13',
             u'PD-Stage 3': u'18', u'Marketing-Stage 6': u'6', u'Marketing-Stage 1': u'1', u'Packaging-Stage 2': u'9',
             u'Packaging - Stage 4': u'11', u'Marketing-Stage 4': u'4', u'Packaging-Stage1': u'8',
             u'PD-Stage 2 W/ R&D': u'16', u'Packaging-Stage3': u'10', u'Marketing-Stage3': u'3', u'PD - Stage 4': u'19',
             u'PD-Stage 2 W/O R&D': u'17', u'PD - Overall Summary': u'21', u'PD - Stage 1': u'15',
             u'Marketing Summary': u'7', u'Packaging Summary': u'14', u'Marketing-Stage 5': u'5'}
    d = {'Yes': 17, 'No': 16}
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "3QVRRWHHJX3D9":
        if body['FormID'] == '15':  # PD - Stage 1
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            # print result_1
            for sub_id in json.loads(result_1)['data']['matchedRows']:
                # print sub_id['FormID']
                for k, v in d.items():
                    if body['FormData']['Similar Products Available'] == k:
                        if v == sub_id['FormID']:
                            submission_id = sub_id['FormSubmissionID']
                            submission_id = str(submission_id)
                            result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                            output = {}
                            output['FormID'] = sub_id['FormID']
                            output['FormSubmissionID'] = sub_id['FormSubmissionID']
                            output['BusinessTag'] = '3QVRRWHHJX3D9'
                            print json.dumps(output)

        elif body['FormID'] == '16':    #PD-Stage 2 W/ R&D
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Product Spec Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  #PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

                    if sub_id['FormID'] == 1:  #Marketing-Stage 1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)

                    if sub_id['FormID'] == 8:  #Packaging-Stage1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)

        elif body['FormID'] == '17':    #PD-Stage 2 W/O R&D
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Product Spec Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  #PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

                    if sub_id['FormID'] == 1:  #Marketing-Stage 1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)

                    if sub_id['FormID'] == 8:  #Packaging-Stage1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)

#****************************************  This Flow Is For Packaging  **************************
        elif body['FormID'] == '8':    #Packaging-Stage1
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Product Feature Spec Ready']=="true" and body['FormData']['Product Attributes Ready']=="true" and body['FormData']['Product Pack Sizes Ready']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 9:  #Packaging-Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '9':    #Packaging-Stage 2
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Are 2D packaging spec ready']=="true" and body['FormData']['Are 3D packaging spec ready']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 10:  #Packaging-Stage3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '10':  # Packaging-Stage 3
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Evaluation Result'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 11:  # Packaging - Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

            elif body['FormData']['Evaluation Result'] == "Suggested changes":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 9:  # Packaging - Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Are 2D packaging spec ready", "Are 3D packaging spec ready"]
                        # result = CM.publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = CM.edit_form_submission(submission_id, field_name, body['BusinessTag'],  BASE_URL, headers1, "false")


        elif body['FormID'] == '11':  # Packaging-Stage 4
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Mock-ups ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 12:  # Packaging-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '12':  # Packaging-Stage 5
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Mockup Evaluation'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 13:  # Packaging-Stage 6
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)


        elif body['FormID'] == '13':  # Packaging-Stage 6
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Packaging Signoff'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Packaging Signoff ready"]
                        # result = CM.edit_form_submission_true(submission_id,field_name,zviceID)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = CM.edit_form_submission(submission_id, field_name, zviceID, BASE_URL, headers1, "true")



#******************************************************************************************************************

#***************************** This Flow Is For Marketing  ********************************************************
        elif body['FormID'] == '1':    # Marketing-Stage 1
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Ideation Done']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 2:  #Marketing-Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id,body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '2':  # Marketing-Stage 2
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Briefing Done'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 3:  # Marketing-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '3':  # Marketing-Stage 3
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Received Creatives'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 4:  # Marketing-Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '4':  # Marketing-Stage 4
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Vetting Result'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 5:  # Marketing-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

            elif body['FormData']['Vetting Result'] == "Suggested Changes":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 3:  # Marketing-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Received Creatives"]
                        # result = CM.publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = CM.edit_form_submission(submission_id, field_name, body['BusinessTag'], BASE_URL, headers1, "false")


        elif body['FormID'] == '5':  # Marketing-Stage 5
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['BOP checking status'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 6:  # Marketing-Stage 6
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '6':  # Marketing-Stage 6
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Shareholders Signoff'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Marketing Signoff Ready"]
                        # result = CM.edit_form_submission_true(submission_id,field_name,zviceID)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = CM.edit_form_submission(submission_id, field_name, zviceID, BASE_URL, headers1, "true")
#*****************************************************************************************************************
#*******************    PD Stage 3  ******************************************************************************

        elif body['FormID'] == '18':  # PD-Stage 3
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['R&D Signoff ready'] == "true" and body['FormData']['Packaging Signoff ready'] == "true" and body['FormData']['Marketing Signoff Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 19:  # PD-Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '19':  # PD-Stage 4
            result_1 = CM.get_submission_id(w_ID, body['BusinessTag'], BASE_URL, headers1)
            if body['FormData']['Trial results'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 20:  # PD-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = CM.publish_submission(submission_id, body['BusinessTag'], BASE_URL, headers1)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            elif body['FormData']['Trial results'] == "Rejected":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["R&D Signoff ready", "Packaging Signoff ready", "Marketing Signoff Ready"]
                        # result = CM.publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = CM.edit_form_submission(submission_id, field_name, body['BusinessTag'], BASE_URL, headers1, "false")

#******************************************************************************************************************


#*************************  this part is giving us Form card id and form submission id related to this work flow

def mainworkflow(body, headers1, BASE_URL):


    try:
        w_ID = body['FormData']['WorkflowID']
        w_ID = str(w_ID)
    except:
        w_ID = 0

    if body['Cmd'] == "workflow-create":
        forms = {u'Packaging-Stage 5': u'12', u'Marketing-Stage2': u'2', u'PD-Stage 5': u'20', u'Packaging-Stage 6': u'13',
         u'PD-Stage 3': u'18', u'Marketing-Stage 6': u'6', u'Marketing-Stage 1': u'1', u'Packaging-Stage 2': u'9',
         u'Packaging - Stage 4': u'11', u'Marketing-Stage 4': u'4', u'Packaging-Stage1': u'8',
         u'PD-Stage 2 W/ R&D': u'16', u'Packaging-Stage3': u'10', u'Marketing-Stage3': u'3', u'PD - Stage 4': u'19',
         u'PD-Stage 2 W/O R&D': u'17', u'PD - Overall Summary': u'21', u'PD - Stage 1': u'15',
         u'Marketing Summary': u'7', u'Packaging Summary': u'14', u'Marketing-Stage 5': u'5'}
        form_id = []
        for k,v in forms.items():
            form_id.append(int(v))
        result = CM.submit_form(body['WorkflowID'], form_id, body['BusinessTag'],  BASE_URL, headers1)
        result_2 = CM.get_submission_id(str(body['WorkflowID']), body['BusinessTag'], BASE_URL, headers1 )
        for sub_id in json.loads(result_2)['data']['matchedRows']:
            if sub_id['FormID'] == int(forms['PD - Stage 1']):
                output = {}
                output['FormID'] = sub_id['FormID']
                output['FormSubmissionID'] = sub_id['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

    elif  body['Cmd'] == "form-submit":
        workflow_genie_1(body, w_ID,  body['BusinessTag'], headers1, BASE_URL)

    elif  body['Cmd'] == "textcard-click" :
        for el in body["Tags"]:
            if el == "MinalText":
                tags = ["Minal", "MinalText"]
                print json.dumps(tags)
