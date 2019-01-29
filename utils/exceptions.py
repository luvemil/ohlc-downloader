class BaseCryptoDownloaderError(Exception):
    """Base error class"""
    pass

class NotAValidTimeZoneError(BaseCryptoDownloaderError):
    """Raise when a timezone is not valid"""
    pass

class NotAValidRoundMethodError(BaseCryptoDownloaderError):
    pass

class EmptyPartitionError(BaseCryptoDownloaderError):
    pass

class NotCompatibleExchange(BaseCryptoDownloaderError):
    pass

class UnknownExchangeError(BaseCryptoDownloaderError):
    pass
