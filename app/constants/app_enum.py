from enum import Enum

class MessageType (str,Enum):
    query= 'query'
    explanation = 'explanation'
    reply='reply'
    chart='chart'
    error = 'error'
    test_query='test_query'
    test_chart='test_chart'


class RoleEnums (str, Enum):
    client='client'
    assistent='assistent'

class ProgressStatus (str, Enum):
    loading='laoding'
    thinking='thinking'
    successs='success'
    error='error'