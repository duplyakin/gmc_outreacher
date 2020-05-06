def construct_prospect_filter(filter_data, filter_fields, without_prefix=[], regex_fields={'column' : 'contains'}, prefix='data__'):
    res = {}

    for k, v in filter_data.items():
        # will use this value later in regexp
        if k in regex_fields.values():
            continue
        
        # only fields that we accept for filter
        if k in filter_fields:
            v = filter_data[k]

            # just pass empty filter
            if v:
                key = str(k)
                if key not in without_prefix:
                    key = prefix + str(k)

                #is it regexp field?
                if k in regex_fields.keys():
                    # the value of the key is the column that we need to regex for
                    key = str(v)
                    if key not in without_prefix:
                        key = prefix + str(v)


                    #get value to regex
                    search_field = regex_fields[k]
                    value = filter_data[search_field]
                    
                    pattern = '{0}'.format(value)

                    regex = {
                        "$regex" : pattern,
                        "$options" : "si"
                    }
                    res[key] = regex
                else:
                    res[key] = v

    return res