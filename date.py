from datetime import datetime

def parse_date(user_input):
    # Try common date formats
    formats = [
        '%Y-%m-%d',    
        '%m/%d/%Y',    
        '%d/%m/%Y',    
        '%d-%m-%Y',    
        '%b %d, %Y',   
    ]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(user_input, fmt)
            return date_obj.strftime('%Y-%m-%d')  # Convert to PostgreSQL format
        except ValueError:
            continue
    
    return None  # If no format matched
