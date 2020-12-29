import sys

'''
    Get path based on system 
'''
def get_proper_path(inputs=[]):
    path = ''
    for i in inputs:
        if inputs.index(i) == 0:
            path += i
            continue
        path += __get_platform_separator()
        path += i
    return path

'''
    Get difrence between two values as percent
'''
def percent_change(new_value, old_value):

    new_value = float(new_value)
    old_value = float(old_value)

    p_change = ((new_value - old_value) / old_value) * 100.00
    return p_change

'''
    Truncate a float without rounding 
'''
def truncate(value, lenght):
    v = str(value).split('.')
    
    nv = ''
    for i in range(lenght):
        nv += v[1][i]
    
    out_v = v[0] + '.' + nv
    
    return float(out_v)


# Private functions 
def __get_platform_separator():
    if sys.platform == 'win32':
        return '\\'
    elif sys.platform == 'linux':
        return '/'
    return '|'

