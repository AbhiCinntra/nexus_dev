# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def remove_whitespace(data):
    if isinstance(data, dict):
        # Remove whitespace from dictionary keys and values
        cleaned_data = {key.strip(): remove_whitespace(value) for key, value in data.items() if key.strip()}
    elif isinstance(data, list):
        # Remove whitespace from list elements
        cleaned_data = [remove_whitespace(item) for item in data]
    elif isinstance(data, str):
        # Remove whitespace from string
        cleaned_data = data.strip()
    else:
        # Return data as is for other types
        cleaned_data = data
    return cleaned_data
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def PAGE(json_data):
    arr={}
    try:
        if str(json_data['maxItem']).lower()=="all":
            endWith=None
            startWith=0
            arr['startWith'] = startWith
            arr['endWith'] = endWith
            return arr
        else:
            PageNo = json_data['PageNo']
            try:
                MaxItem = int(json_data['maxItem'])
            except:
                MaxItem = 10
            endWith = (PageNo * MaxItem)
            startWith = (endWith - MaxItem)

            arr['startWith'] = startWith
            arr['endWith'] = endWith
            return arr
    except Exception as e:
        print(str(e))
        return str(e)