from datetime import datetime, timezone


class DatetimeUtil:
    @staticmethod
    def get_iso8601_format(timestamp):
        return datetime.fromtimestamp(timestamp//1000,timezone.utc).replace(microsecond=timestamp%1000*1000).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
def timestamp(dt:datetime) -> int:
    return int(dt.timestamp() * 1000)

def current_timestamp():
    return timestamp(datetime.now())

def get_local_timezone_offset() -> str:
    td_in_seconds = datetime.now().astimezone().tzinfo.utcoffset(None).total_seconds()
    hours, remainder = divmod(td_in_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    sign = '-' if td_in_seconds < 0 else '+'

    return f"{sign}{int(hours):02}:{int(minutes):02}"