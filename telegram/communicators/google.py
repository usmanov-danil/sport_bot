import sqlite3
from contextlib import closing
from pathlib import Path

from loguru import logger
from octopus.communicators.abstract import Communicator
from octopus.models.base import Interval
from octopus.models.infrastructure import TRAFFIC_TIMASTAMP_FORMAT, TrafficDataFormat


class SQLiteCommunicator(Communicator):
    def pull_data(self, interval: Interval) -> list[TrafficDataFormat]:
        data = []
        for target in self.targets:
            if not target.db_path:
                raise ValueError('db_path must be set for communication target')
            try:
                data += self._grab_db_data(target.db_path, interval)
            except Exception as e:
                logger.error('Error during grabbing data from external dbs: {}', e)

        return data

    @staticmethod
    def _grab_db_data(db: Path, interval: Interval) -> list[TrafficDataFormat]:
        connection = sqlite3.connect(db)

        with closing(connection.cursor()) as cursor:
            query = f'SELECT data FROM measurements_local WHERE \
                timestamp > "{interval.start_time.strftime(TRAFFIC_TIMASTAMP_FORMAT)}" \
                AND timestamp <= "{interval.last_time.strftime(TRAFFIC_TIMASTAMP_FORMAT)}"'
            logger.debug('Next SQL query: {}', query)
            cursor.execute(query)
            data = [entry[0] for entry in cursor.fetchall()]

        connection.close()
        return [TrafficDataFormat.parse_raw(entry) for entry in data]
