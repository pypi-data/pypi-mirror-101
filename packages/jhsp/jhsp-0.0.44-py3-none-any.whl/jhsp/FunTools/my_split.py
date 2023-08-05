import re

def split(ori_str,seps):

    standard_sep = '!@#$%^&'
    pattern = re.compile(str(seps))
    new_str = re.sub(pattern,standard_sep,ori_str)
    split_str_list = new_str.split(standard_sep)
    
    return split_str_list

