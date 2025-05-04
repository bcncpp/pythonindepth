class DataTransport:
    """An example of an object that separates the exception handling by abstraction levels."""
    _RETRY_BACKOFF: int = 5
    _RETRY_TIMES: int = 3

    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self.connection = None

    def deliver_event(self, event: Event):
        try:
            self.connection = connect_with_retry(
                self._connector,
                self._RETRY_TIMES,
                self._RETRY_BACKOFF
            )
            self.send(event)
        except Exception as e:
            raise RuntimeError("Failed to deliver event") from e

    def send(self, event: Event):
        try:
            return self.connection.send(event.decode())
        except ValueError as e:
            logger.error("%r contains incorrect data: %s", event, e)
            raise DataEncodingError(f"Failed to decode event: {event}") from e


class DataEncodingError(Exception):
    """Custom exception for event decoding errors."""
       pass

