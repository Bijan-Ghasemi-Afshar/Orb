from orb.KB import fault_kb

'''
Goal: Handles user intention to report an issue.

Action: Sends user input to Fault Kowledge Base in order to 
retrieve the link to fault reporting system based on the system knowledge.
(Has to implement the logic to get fault information form the user in the future)
'''
def response(user_input):
    fault_kowledge_base = fault_kb.fault_kb(user_input)
    return fault_kowledge_base.get_fault_report_link()