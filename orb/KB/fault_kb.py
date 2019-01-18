'''
Holds knowledge about the process of reporting a fault
(Must retrieve information about the fault in the future)
'''
class fault_kb:

    def __init__(self, user_input):
        self.user_input = user_input

    '''
    Provides the link to fault reporting website
    '''
    def get_fault_report_link(self):
        return '<a href=\"http://traintesting.epizy.com\" target=\"_blank\">Report Fault</a>'