from app.storage.sqlite.table.column import Column, Constraint, DataType, ForeignKey
from app.storage.sqlite.table.column_enum import CREATED_DATE, ID
from app.storage.sqlite.table.model import SqliteModel


class ScheduledJob(SqliteModel):
    __databasename__ = 'schedule'
    __tablename__ = 'scheduled_job'

    name = Column(DataType.TEXT, Constraint.UNIQUE)
    scheduled_module_name = Column(DataType.TEXT)
    scheduled_class_name = Column(DataType.TEXT)
    executable = Column(DataType.TEXT)
    arguments = Column(DataType.TEXT)
    last_run_time = Column(DataType.INTEGER)
    next_run_time = Column(DataType.INTEGER)
    frequency = Column(DataType.TEXT)
    start_time = Column(DataType.INTEGER)
    deleted_time = Column(DataType.INTEGER)

class ExecutionHistory(SqliteModel):
    __databasename__ = 'schedule'
    __tablename__ = 'execution_history'

    status = Column(DataType.TEXT)
    run_start_time = Column(DataType.INTEGER)
    run_end_time = Column(DataType.INTEGER)
    message = Column(DataType.TEXT)
    scheduled_job_id = Column(DataType.INTEGER, ForeignKey(ScheduledJob))

    @classmethod
    def select_all_with_scheduled_job(cls):
        query = f'SELECT *, {ScheduledJob.__tablename__}.name as scheduled_job_name FROM {cls.__tablename__} JOIN {ScheduledJob.__tablename__} ON {cls.__tablename__}.scheduled_job_id = {ScheduledJob.__tablename__}.{ID} ORDER BY {cls.__tablename__}.{CREATED_DATE} desc'

        return cls.select_from_query(query)