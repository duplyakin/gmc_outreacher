export default {
    'filter_data' : '',
    'condition_data' : '',
    'value_data' : '',
    'filters' : [
        {
            'id' : 1,
            'type' : 'String',
            'name' : 'Email' 
        },
        {
            'id' : 2,
            'type' : 'Number',
            'name' : 'Last contacted'
        },
        {
            'id' : 3,
            'type' : 'Date',
            'name' : 'Created at'
        }
    ],
    'conditions' : {
        'String' : ['Contains', 'Not contains', 'Equals', 'Not equals'],
        'Number' : ['Equals', 'Greater than', 'Less than'],
        'Date' : ['is']
    }
}