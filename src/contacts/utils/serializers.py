from datetime import date

def serialise_datetime(obj): 
    if isinstance(obj, date): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 