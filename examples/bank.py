#from monads import maybe_m

#bind = maybe_m.bind
#unit = maybe_m.unit



def get_account(name):
    if name == "Irek": return 1
    elif name == "John": return 2
    else: return None

def get_balance(account):
    if account == 1: return 1000000
    elif account == 2: return 75000
    else: return None

def get_qualified_amount(balance):
    if balance > 200000: return balance
    else: return None



def bind(v, f):
    if (v):
        return f(v)
    else:
        return None



def get_loan(name):
    m_account = get_account(name)
    m_balance = bind(m_account, get_balance)
    m_loan =    bind(m_balance, get_qualified_amount)
    return m_loan
