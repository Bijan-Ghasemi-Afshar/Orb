from orb.KB import fault_kb

def response(user_input):
    fault_kowledge_base = fault_kb.fault_kb(user_input)
    return fault_kowledge_base.get_fault_report_link()