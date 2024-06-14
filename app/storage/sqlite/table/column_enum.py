from enum import Enum


class SystemColumn(Enum):
    id = 'up__id'
    created_date = 'up__created_date'
    last_modified_date = 'up__last_modified_date'

    @classmethod
    def list(cls):
        return [member.value for member in cls]
    
    @classmethod
    def dict(cls):
        return {member.name: member.value for member in cls}
    
ID = SystemColumn.id.value
CREATED_DATE = SystemColumn.created_date.value
LAST_MODIFIED_DATE = SystemColumn.last_modified_date.value