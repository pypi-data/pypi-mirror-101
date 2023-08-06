import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Auxiliary
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Securities
import System
import System.Collections
import System.Collections.Generic

QuantConnect_Data_Auxiliary_MapFileRow = typing.Any
QuantConnect_Data_Auxiliary_MapFileResolver_MapFileRowEntry = typing.Any


class MapFileRow(System.Object, System.IEquatable[QuantConnect_Data_Auxiliary_MapFileRow]):
    """Represents a single row in a map_file. This is a csv file ordered as {date, mapped symbol}"""

    @property
    def Date(self) -> datetime.datetime:
        """Gets the date associated with this data"""
        ...

    @property
    def MappedSymbol(self) -> str:
        """Gets the mapped symbol"""
        ...

    @property
    def PrimaryExchange(self) -> int:
        """
        Gets the mapped symbol
        
        This property contains the int value of a member of the QuantConnect.PrimaryExchange enum.
        """
        ...

    @typing.overload
    def __init__(self, date: typing.Union[datetime.datetime, datetime.date], mappedSymbol: str, primaryExchange: str = ...) -> None:
        """Initializes a new instance of the MapFileRow class."""
        ...

    @typing.overload
    def __init__(self, date: typing.Union[datetime.datetime, datetime.date], mappedSymbol: str, primaryExchange: QuantConnect.PrimaryExchange) -> None:
        """Initializes a new instance of the MapFileRow class."""
        ...

    @typing.overload
    def Equals(self, other: QuantConnect.Data.Auxiliary.MapFileRow) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified System.Object is equal to the current System.Object.
        
        :param obj: The object to compare with the current object.
        :returns: true if the specified object  is equal to the current object; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a particular type.
        
        :returns: A hash code for the current System.Object.
        """
        ...

    @staticmethod
    def Parse(line: str) -> QuantConnect.Data.Auxiliary.MapFileRow:
        """Parses the specified line into a MapFileRow"""
        ...

    @staticmethod
    @typing.overload
    def Read(permtick: str, market: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]:
        """Reads in the map_file for the specified equity symbol"""
        ...

    @staticmethod
    @typing.overload
    def Read(path: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]:
        """Reads in the map_file at the specified path"""
        ...

    def ToCsv(self) -> str:
        ...

    def ToString(self) -> str:
        """
        Convert this row into string form
        
        :returns: resulting string.
        """
        ...


class FactorFileRow(System.Object):
    """Defines a single row in a factor_factor file. This is a csv file ordered as {date, price factor, split factor, reference price}"""

    @property
    def Date(self) -> datetime.datetime:
        """Gets the date associated with this data"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """Gets the date associated with this data"""
        ...

    @property
    def PriceFactor(self) -> float:
        """Gets the price factor associated with this data"""
        ...

    @PriceFactor.setter
    def PriceFactor(self, value: float):
        """Gets the price factor associated with this data"""
        ...

    @property
    def SplitFactor(self) -> float:
        """Gets the split factor associated with the date"""
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        """Gets the split factor associated with the date"""
        ...

    @property
    def PriceScaleFactor(self) -> float:
        """Gets the combined factor used to create adjusted prices from raw prices"""
        ...

    @PriceScaleFactor.setter
    def PriceScaleFactor(self, value: float):
        """Gets the combined factor used to create adjusted prices from raw prices"""
        ...

    @property
    def ReferencePrice(self) -> float:
        """Gets the raw closing value from the trading date before the updated factor takes effect"""
        ...

    @ReferencePrice.setter
    def ReferencePrice(self, value: float):
        """Gets the raw closing value from the trading date before the updated factor takes effect"""
        ...

    def __init__(self, date: typing.Union[datetime.datetime, datetime.date], priceFactor: float, splitFactor: float, referencePrice: float = 0) -> None:
        """Initializes a new instance of the FactorFileRow class"""
        ...

    @typing.overload
    def Apply(self, dividend: QuantConnect.Data.Market.Dividend, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """
        Applies the dividend to this factor file row.
        This dividend date must be on or before the factor
        file row date
        
        :param dividend: The dividend to apply with reference price and distribution specified
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file row that applies the dividend to this row's factors.
        """
        ...

    @typing.overload
    def Apply(self, split: QuantConnect.Data.Market.Split, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """
        Applies the split to this factor file row.
        This split date must be on or before the factor
        file row date
        
        :param split: The split to apply with reference price and split factor specified
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file row that applies the split to this row's factors.
        """
        ...

    def GetDividend(self, futureFactorFileRow: QuantConnect.Data.Auxiliary.FactorFileRow, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, decimalPlaces: int = 2) -> QuantConnect.Data.Market.Dividend:
        """
        Creates a new dividend from this factor file row and the one chronologically in front of it
        This dividend may have a distribution of zero if this row doesn't represent a dividend
        
        :param futureFactorFileRow: The next factor file row in time
        :param symbol: The symbol to use for the dividend
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :param decimalPlaces: The number of decimal places to round the dividend's distribution to, defaulting to 2
        :returns: A new dividend instance.
        """
        ...

    def GetSplit(self, futureFactorFileRow: QuantConnect.Data.Auxiliary.FactorFileRow, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Market.Split:
        """
        Creates a new split from this factor file row and the one chronologically in front of it
        This split may have a split factor of one if this row doesn't represent a split
        
        :param futureFactorFileRow: The next factor file row in time
        :param symbol: The symbol to use for the split
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new split instance.
        """
        ...

    @staticmethod
    def Parse(lines: System.Collections.Generic.IEnumerable[str], factorFileMinimumDate: typing.Optional[typing.Optional[datetime.datetime]]) -> typing.Union[System.Collections.Generic.List[QuantConnect.Data.Auxiliary.FactorFileRow], typing.Optional[datetime.datetime]]:
        """
        Parses the lines as factor files rows while properly handling inf entries
        
        :param lines: The lines from the factor file to be parsed
        :param factorFileMinimumDate: The minimum date from the factor file
        :returns: An enumerable of factor file rows.
        """
        ...

    @staticmethod
    def Read(permtick: str, market: str, factorFileMinimumDate: typing.Optional[typing.Optional[datetime.datetime]]) -> typing.Union[System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow], typing.Optional[datetime.datetime]]:
        """Reads in the factor file for the specified equity symbol"""
        ...

    def ToCsv(self, source: str = None) -> str:
        """Writes this row to csv format"""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class MapFile(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow], typing.Iterable[QuantConnect.Data.Auxiliary.MapFileRow]):
    """Represents an entire map file for a specified symbol"""

    @property
    def Permtick(self) -> str:
        """Gets the entity's unique symbol, i.e OIH.1"""
        ...

    @property
    def DelistingDate(self) -> datetime.datetime:
        """Gets the last date in the map file which is indicative of a delisting event"""
        ...

    @property
    def FirstDate(self) -> datetime.datetime:
        """Gets the first date in this map file"""
        ...

    @property
    def FirstTicker(self) -> str:
        """Gets the first ticker for the security represented by this map file"""
        ...

    def __init__(self, permtick: str, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFileRow]) -> None:
        """Initializes a new instance of the MapFile class."""
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.MapFileRow]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    @staticmethod
    def GetMapFilePath(permtick: str, market: str) -> str:
        """
        Constructs the map file path for the specified market and symbol
        
        :param permtick: The symbol as on disk, OIH or OIH.1
        :param market: The market this symbol belongs to
        :returns: The file path to the requested map file.
        """
        ...

    @staticmethod
    def GetMapFiles(mapFileDirectory: str) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile]:
        ...

    def GetMappedSymbol(self, searchDate: typing.Union[datetime.datetime, datetime.date], defaultReturnValue: str = ...) -> str:
        """
        Memory overload search method for finding the mapped symbol for this date.
        
        :param searchDate: date for symbol we need to find.
        :param defaultReturnValue: Default return value if search was got no result.
        :returns: Symbol on this date.
        """
        ...

    def HasData(self, date: typing.Union[datetime.datetime, datetime.date]) -> bool:
        """Determines if there's data for the requested date"""
        ...

    @staticmethod
    def Read(permtick: str, market: str) -> QuantConnect.Data.Auxiliary.MapFile:
        """Reads in an entire map file for the requested symbol from the DataFolder"""
        ...

    def ToCsvLines(self) -> System.Collections.Generic.IEnumerable[str]:
        """
        Reads and writes each MapFileRow
        
        :returns: Enumerable of csv lines.
        """
        ...

    def WriteToCsv(self, market: str) -> None:
        """
        Writes the map file to a CSV file
        
        :param market: The market to save the MapFile to
        """
        ...


class MapFileResolver(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile], typing.Iterable[QuantConnect.Data.Auxiliary.MapFile]):
    """
    Provides a means of mapping a symbol at a point in time to the map file
    containing that share class's mapping information
    """

    class MapFileRowEntry(System.Object, System.IEquatable[QuantConnect_Data_Auxiliary_MapFileResolver_MapFileRowEntry]):
        """Combines the map file row with the map file path that produced the row"""

        @property
        def MapFileRow(self) -> QuantConnect.Data.Auxiliary.MapFileRow:
            """Gets the map file row"""
            ...

        @MapFileRow.setter
        def MapFileRow(self, value: QuantConnect.Data.Auxiliary.MapFileRow):
            """Gets the map file row"""
            ...

        @property
        def EntitySymbol(self) -> str:
            """Gets the full path to the map file that produced this row"""
            ...

        @EntitySymbol.setter
        def EntitySymbol(self, value: str):
            """Gets the full path to the map file that produced this row"""
            ...

        def __init__(self, entitySymbol: str, mapFileRow: QuantConnect.Data.Auxiliary.MapFileRow) -> None:
            """
            Initializes a new instance of the MapFileRowEntry class
            
            :param entitySymbol: The map file that produced this row
            :param mapFileRow: The map file row data
            """
            ...

        def Equals(self, other: QuantConnect.Data.Auxiliary.MapFileResolver.MapFileRowEntry) -> bool:
            """
            Indicates whether the current object is equal to another object of the same type.
            
            :param other: An object to compare with this object.
            :returns: true if the current object is equal to the  parameter; otherwise, false.
            """
            ...

        def ToString(self) -> str:
            """
            Returns a string that represents the current object.
            
            :returns: A string that represents the current object.
            """
            ...

    Empty: QuantConnect.Data.Auxiliary.MapFileResolver = ...
    """
    Gets an empty MapFileResolver, that is an instance that contains
    zero mappings
    """

    def __init__(self, mapFiles: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.MapFile]) -> None:
        """
        Initializes a new instance of the MapFileResolver by reading
        in all files in the specified directory.
        
        :param mapFiles: The data used to initialize this resolver.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(dataDirectory: str, market: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Creates a new instance of the MapFileResolver class by reading all map files
        for the specified market into memory
        
        :param dataDirectory: The root data directory
        :param market: The equity market to produce a map file collection for
        :returns: The collection of map files capable of mapping equity symbols within the specified market.
        """
        ...

    @staticmethod
    @typing.overload
    def Create(mapFileDirectory: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Creates a new instance of the MapFileResolver class by reading all map files
        for the specified market into memory
        
        :param mapFileDirectory: The directory containing the map files
        :returns: The collection of map files capable of mapping equity symbols within the specified market.
        """
        ...

    def GetByPermtick(self, permtick: str) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Gets the map file matching the specified permtick
        
        :param permtick: The permtick to match on
        :returns: The map file matching the permtick, or null if not found.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.MapFile]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    def ResolveMapFile(self, symbol: str, date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Resolves the map file path containing the mapping information for the symbol defined at
        
        :param symbol: The symbol as of  to be mapped
        :param date: The date associated with the
        :returns: The map file responsible for mapping the symbol, if no map file is found, null is returned.
        """
        ...


class QuoteConditionFlags(System.Enum):
    """Flag system for quote conditions"""

    # Cannot convert to Python: None = 0
    """No Condition"""

    Regular = ...
    """This condition is used for the majority of quotes to indicate a normal trading environment."""

    Slow = ...
    """
    This condition is used to indicate that the quote is a Slow Quote on both the Bid and Offer
    sides due to a Set Slow List that includes High Price securities.
    """

    Gap = ...
    """
    While in this mode, auto-execution is not eligible, the quote is then considered manual and non-firm in the Bid and Offer and
    either or both sides can be traded through as per Regulation NMS.
    """

    Closing = ...
    """This condition can be disseminated to indicate that this quote was the last quote for a security for that Participant."""

    NewsDissemination = ...
    """
    This regulatory Opening Delay or Trading Halt is used when relevant news influencing the security is being disseminated.
    Trading is suspended until the primary market determines that an adequate publication or disclosure of information has occurred.
    """

    NewsPending = ...
    """
    This condition is used to indicate a regulatory Opening Delay or Trading Halt due to an expected news announcement,
    which may influence the security. An Opening Delay or Trading Halt may be continued once the news has been disseminated.
    """

    TradingRangeIndication = ...
    """
    The condition is used to denote the probable trading range (bid and offer prices, no sizes) of a security that is not Opening Delayed or
    Trading Halted. The Trading Range Indication is used prior to or after the opening of a security.
    """

    OrderImbalance = ...
    """This non-regulatory Opening Delay or Trading Halt is used when there is a significant imbalance of buy or sell orders."""

    ClosedMarketMaker = ...
    """
    This condition is disseminated by each individual FINRA Market Maker to signify either the last quote of the day or
    the premature close of an individual Market Maker for the day.
    """

    VolatilityTradingPause = ...
    """
    This quote condition indicates a regulatory Opening Delay or Trading Halt due to conditions in which
    a security experiences a 10 % or more change in price over a five minute period.
    """

    NonFirmQuote = ...
    """This quote condition suspends a Participant's firm quote obligation for a quote for a security."""

    OpeningQuote = ...
    """This condition can be disseminated to indicate that this quote was the opening quote for a security for that Participant."""

    DueToRelatedSecurity = ...
    """
    This non-regulatory Opening Delay or Trading Halt is used when events relating to one security will affect the price and performance of
    another related security. This non-regulatory Opening Delay or Trading Halt is also used when non-regulatory halt reasons such as
    Order Imbalance, Order Influx and Equipment Changeover are combined with Due to Related Security on CTS.
    """

    Resume = ...
    """
    This quote condition along with zero-filled bid, offer and size fields is used to indicate that trading for a Participant is no longer
    suspended in a security which had been Opening Delayed or Trading Halted.
    """

    InViewOfCommon = ...
    """
    This quote condition is used when matters affecting the common stock of a company affect the performance of the non-common
    associated securities, e.g., warrants, rights, preferred, classes, etc.
    """

    EquipmentChangeover = ...
    """
    This non-regulatory Opening Delay or Trading Halt is used when the ability to trade a security by a Participant is temporarily
    inhibited due to a systems, equipment or communications facility problem or for other technical reasons.
    """

    SubPennyTrading = ...
    """
    This non-regulatory Opening Delay or Trading Halt is used to indicate an Opening Delay or Trading Halt for a security whose price
    may fall below $1.05, possibly leading to a sub-penny execution.
    """

    NoOpenNoResume = ...
    """
    This quote condition is used to indicate that an Opening Delay or a Trading Halt is to be in effect for the rest
    of the trading day in a security for a Participant.
    """

    LimitUpLimitDownPriceBand = ...
    """This quote condition is used to indicate that a Limit Up-Limit Down Price Band is applicable for a security."""

    RepublishedLimitUpLimitDownPriceBand = ...
    """
    This quote condition is used to indicate that a Limit Up-Limit Down Price Band that is being disseminated " +
    is a ‘republication’ of the latest Price Band for a security.
    """

    Manual = ...
    """
    This indicates that the market participant is in a manual mode on both the Bid and Ask. While in this mode,
    automated execution is not eligible on the Bid and Ask side and can be traded through pursuant to Regulation NMS requirements.
    """

    FastTrading = ...
    """For extremely active periods of short duration. While in this mode, the UTP participant will enter quotations on a “best efforts” basis."""

    OrderInflux = ...
    """A halt condition used when there is a sudden order influx. To prevent a disorderly market, trading is temporarily suspended by the UTP participant."""


class LocalDiskMapFileProvider(System.Object, QuantConnect.Interfaces.IMapFileProvider):
    """
    Provides a default implementation of IMapFileProvider that reads from
    the local disk
    """

    def Get(self, market: str) -> QuantConnect.Data.Auxiliary.MapFileResolver:
        """
        Gets a MapFileResolver representing all the map
        files for the specified market
        
        :param market: The equity market, for example, 'usa'
        :returns: A MapFileRow containing all map files for the specified market.
        """
        ...


class TradeConditionFlags(System.Enum):
    """Flag system for trade conditions"""

    # Cannot convert to Python: None = 0
    """No Condition"""

    Regular = ...
    """A trade made without stated conditions is deemed regular way for settlement on the third business day following the transaction date."""

    Cash = ...
    """A transaction which requires delivery of securities and payment on the same day the trade takes place."""

    NextDay = ...
    """A transaction that requires the delivery of securities on the first business day following the trade date."""

    Seller = ...
    """
    A Seller’s Option transaction gives the seller the right to deliver the security at any time within a specific period,
    ranging from not less than two calendar days, to not more than sixty calendar days.
    """

    YellowFlag = ...
    """
    Market Centers will have the ability to identify regular trades being reported during specific events as out of the ordinary
    by appending a new sale condition code Yellow Flag (Y) on each transaction reported to the UTP SIP.
    The new sale condition will be eligible to update all market center and consolidated statistics.
    """

    IntermarketSweep = ...
    """The transaction that constituted the trade-through was the execution of an order identified as an Intermarket Sweep Order."""

    OpeningPrints = ...
    """The trade that constituted the trade-through was a single priced opening transaction by the Market Center."""

    ClosingPrints = ...
    """The transaction that constituted the trade-through was a single priced closing transaction by the Market Center."""

    ReOpeningPrints = ...
    """The trade that constituted the trade-through was a single priced reopening transaction by the Market Center."""

    DerivativelyPriced = ...
    """
    The transaction that constituted the trade-through was the execution of an order at a price that was not based, directly or indirectly,
    on the quoted price of the security at the time of execution and for which the material terms were not reasonably determinable
    at the time the commitment to execute the order was made.
    """

    FormT = ...
    """
    Trading in extended hours enables investors to react quickly to events that typically occur outside regular market hours, such as earnings reports.
    However, liquidity may be constrained during such Form T trading, resulting in wide bid-ask spreads.
    """

    Sold = ...
    """Sold Last is used when a trade prints in sequence but is reported late or printed in conformance to the One or Two Point Rule."""

    Stopped = ...
    """
    The transaction that constituted the trade-through was the execution by a trading center of an order for which, at the time
    of receipt of the order, the execution at no worse than a specified price a 'stopped order'
    """

    ExtendedHours = ...
    """Identifies a trade that was executed outside of regular primary market hours and is reported as an extended hours trade."""

    OutOfSequence = ...
    """Identifies a trade that takes place outside of regular market hours."""

    Split = ...
    """
    An execution in two markets when the specialist or Market Maker in the market first receiving the order agrees to execute a portion of it
    at whatever price is realized in another market to which the balance of the order is forwarded for execution.
    """

    Acquisition = ...
    """A transaction made on the Exchange as a result of an Exchange acquisition."""

    Bunched = ...
    """
    A trade representing an aggregate of two or more regular trades in a security occurring at the same price either simultaneously
    or within the same 60-second period, with no individual trade exceeding 10,000 shares.
    """

    StockOption = ...
    """
    Stock-Option Trade is used to identify cash equity transactions which are related to options transactions and therefore
    potentially subject to cancellation if market conditions of the options leg(s) prevent the execution of the stock-option
    order at the price agreed upon.
    """

    Distribution = ...
    """Sale of a large block of stock in such a manner that the price is not adversely affected."""

    AveragePrice = ...
    """A trade where the price reported is based upon an average of the prices for transactions in a security during all or any portion of the trading day."""

    Cross = ...
    """Indicates that the trade resulted from a Market Center’s crossing session."""

    PriceVariation = ...
    """Indicates a regular market session trade transaction that carries a price that is significantly away from the prevailing consolidated or primary market value at the time of the transaction."""

    Rule155 = ...
    """To qualify as a NYSE AMEX Rule 155"""

    OfficialClose = ...
    """Indicates the ‘Official’ closing value as determined by a Market Center. This transaction report will contain the market center generated closing price."""

    PriorReferencePrice = ...
    """
    A sale condition that identifies a trade based on a price at a prior point in time i.e. more than 90 seconds prior to the time of the trade report.
    The execution time of the trade will be the time of the prior reference price.
    """

    OfficialOpen = ...
    """Indicates the ‘Official’ open value as determined by a Market Center. This transaction report will contain the market"""

    CapElection = ...
    """
    The CAP Election Trade highlights sales as a result of a sweep execution on the NYSE, whereby CAP orders have been elected and executed
    outside the best price bid or offer and the orders appear as repeat trades at subsequent execution prices.
    This indicator provides additional information to market participants that an automatic sweep transaction has occurred with repeat
    trades as one continuous electronic transaction.
    """

    AutoExecution = ...
    """A sale condition code that identifies a NYSE trade that has been automatically executed without the potential benefit of price improvement."""

    TradeThroughExempt = ...
    """
    Denotes whether or not a trade is exempt (Rule 611) and when used jointly with certain Sale Conditions,
    will more fully describe the characteristics of a particular trade.
    """

    UndocumentedFlag = ...
    """This flag is present in raw data, but AlgoSeek document does not describe it."""

    OddLot = ...
    """Denotes the trade is an odd lot less than a 100 shares."""


class MapFilePrimaryExchangeProvider(System.Object, QuantConnect.Interfaces.IPrimaryExchangeProvider):
    """Implementation of IPrimaryExchangeProvider from map files."""

    def __init__(self, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider) -> None:
        """
        Constructor for Primary Exchange Provider from MapFiles
        
        :param mapFileProvider: MapFile to use
        """
        ...

    def GetPrimaryExchange(self, securityIdentifier: QuantConnect.SecurityIdentifier) -> int:
        """
        Gets the primary exchange for a given security identifier
        
        :param securityIdentifier: The security identifier to get the primary exchange for
        :returns: Returns the primary exchange or null if not found. This method returns the int value of a member of the QuantConnect.PrimaryExchange enum.
        """
        ...


class MappingExtensions(System.Object):
    """Mapping extensions helper methods"""

    @staticmethod
    def ResolveMapFile(mapFileResolver: QuantConnect.Data.Auxiliary.MapFileResolver, symbol: typing.Union[QuantConnect.Symbol, str], dataType: typing.Type) -> QuantConnect.Data.Auxiliary.MapFile:
        """
        Helper method to resolve the mapping file to use.
        
        :param mapFileResolver: The map file resolver
        :param symbol: The symbol that we want to map
        :param dataType: The configuration data type SubscriptionDataConfig.Type
        :returns: The mapping file to use.
        """
        ...


class FactorFile(System.Object, System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow], typing.Iterable[QuantConnect.Data.Auxiliary.FactorFileRow]):
    """Represents an entire factor file for a specified symbol"""

    @property
    def SortedFactorFileData(self) -> System.Collections.Generic.SortedList[datetime.datetime, QuantConnect.Data.Auxiliary.FactorFileRow]:
        """The factor file data rows sorted by date"""
        ...

    @SortedFactorFileData.setter
    def SortedFactorFileData(self, value: System.Collections.Generic.SortedList[datetime.datetime, QuantConnect.Data.Auxiliary.FactorFileRow]):
        """The factor file data rows sorted by date"""
        ...

    @property
    def FactorFileMinimumDate(self) -> typing.Optional[datetime.datetime]:
        """The minimum tradeable date for the symbol"""
        ...

    @FactorFileMinimumDate.setter
    def FactorFileMinimumDate(self, value: typing.Optional[datetime.datetime]):
        """The minimum tradeable date for the symbol"""
        ...

    @property
    def MostRecentFactorChange(self) -> datetime.datetime:
        """Gets the most recent factor change in the factor file"""
        ...

    @property
    def Permtick(self) -> str:
        """Gets the symbol this factor file represents"""
        ...

    def __init__(self, permtick: str, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Auxiliary.FactorFileRow], factorFileMinimumDate: typing.Optional[datetime.datetime] = None) -> None:
        """Initializes a new instance of the FactorFile class."""
        ...

    def Apply(self, data: System.Collections.Generic.List[QuantConnect.Data.BaseData], exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> QuantConnect.Data.Auxiliary.FactorFile:
        """
        Creates a new factor file with the specified data applied.
        Only Dividend and Split data types
        will be used.
        
        :param data: The data to apply
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :returns: A new factor file that incorporates the specified dividend.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Auxiliary.FactorFileRow]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    def GetPriceScaleFactor(self, searchDate: typing.Union[datetime.datetime, datetime.date]) -> float:
        """Gets the price scale factor that includes dividend and split adjustments for the specified search date"""
        ...

    def GetScalingFactors(self, searchDate: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Data.Auxiliary.FactorFileRow:
        """Gets price and split factors to be applied at the specified date"""
        ...

    def GetSplitFactor(self, searchDate: typing.Union[datetime.datetime, datetime.date]) -> float:
        """Gets the split factor to be applied at the specified date"""
        ...

    def GetSplitsAndDividends(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, decimalPlaces: int = 2) -> System.Collections.Generic.List[QuantConnect.Data.BaseData]:
        """
        Gets all of the splits and dividends represented by this factor file
        
        :param symbol: The symbol to ues for the dividend and split objects
        :param exchangeHours: Exchange hours used for resolving the previous trading day
        :param decimalPlaces: The number of decimal places to round the dividend's distribution to, defaulting to 2
        :returns: All splits and diviends represented by this factor file in chronological order.
        """
        ...

    def HasDividendEventOnNextTradingDay(self, date: typing.Union[datetime.datetime, datetime.date], priceFactorRatio: typing.Optional[float], referencePrice: typing.Optional[float]) -> typing.Union[bool, float, float]:
        """
        Returns true if the specified date is the last trading day before a dividend event
        is to be fired
        
        :param date: The date to check the factor file for a dividend event
        :param priceFactorRatio: When this function returns true, this value will be populated with the price factor ratio required to scale the closing value (pf_i/pf_i+1)
        :param referencePrice: When this function returns true, this value will be populated with the reference raw price, which is the close of the provided date
        """
        ...

    @staticmethod
    def HasScalingFactors(permtick: str, market: str) -> bool:
        """Checks whether or not a symbol has scaling factors"""
        ...

    def HasSplitEventOnNextTradingDay(self, date: typing.Union[datetime.datetime, datetime.date], splitFactor: typing.Optional[float], referencePrice: typing.Optional[float]) -> typing.Union[bool, float, float]:
        """
        Returns true if the specified date is the last trading day before a split event
        is to be fired
        
        :param date: The date to check the factor file for a split event
        :param splitFactor: When this function returns true, this value will be populated with the split factor ratio required to scale the closing value
        :param referencePrice: When this function returns true, this value will be populated with the reference raw price, which is the close of the provided date
        """
        ...

    @staticmethod
    def Parse(permtick: str, lines: System.Collections.Generic.IEnumerable[str]) -> QuantConnect.Data.Auxiliary.FactorFile:
        """Parses the specified lines as a factor file"""
        ...

    @staticmethod
    def Read(permtick: str, market: str) -> QuantConnect.Data.Auxiliary.FactorFile:
        """Reads a FactorFile in from the Globals.DataFolder."""
        ...

    def ToCsvLines(self) -> System.Collections.Generic.IEnumerable[str]:
        """
        Writes this factor file data to an enumerable of csv lines
        
        :returns: An enumerable of lines representing this factor file.
        """
        ...

    def WriteToCsv(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Write the factor file to the correct place in the default Data folder
        
        :param symbol: The symbol this factor file represents
        """
        ...


class LocalDiskFactorFileProvider(System.Object, QuantConnect.Interfaces.IFactorFileProvider):
    """Provides an implementation of IFactorFileProvider that searches the local disk"""

    @typing.overload
    def __init__(self) -> None:
        """
        Initializes a new instance of LocalDiskFactorFileProvider that uses configuration
        to resolve an instance of IMapFileProvider from the Composer.Instance
        """
        ...

    @typing.overload
    def __init__(self, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider) -> None:
        """
        Initializes a new instance of the LocalDiskFactorFileProvider using the specified
        map file provider
        
        :param mapFileProvider: The map file provider used to resolve permticks of securities
        """
        ...

    def Get(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.Auxiliary.FactorFile:
        """
        Gets a FactorFile instance for the specified symbol, or null if not found
        
        :param symbol: The security's symbol whose factor file we seek
        :returns: The resolved factor file, or null if not found.
        """
        ...


class ZipEntryName(QuantConnect.Data.BaseData):
    """Defines a data type that just produces data points from the zip entry names in a zip file"""

    def __init__(self) -> None:
        """Initializes a new instance of the ZipEntryName class"""
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method, and returns a new instance of the object
        each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...


