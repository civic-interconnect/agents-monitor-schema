# Module `agents_monitor_schema.parsers.openstates_parser`

## Classes

### `AIOHTTPTransport(self, url: str, headers: Union[Mapping[str, str], Mapping[multidict._multidict.istr, str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, Iterable[Tuple[Union[str, multidict._multidict.istr], str]], NoneType] = None, cookies: Union[Mapping[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]], Iterable[Tuple[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]]], ForwardRef('BaseCookie[str]'), NoneType] = None, auth: Union[aiohttp.helpers.BasicAuth, ForwardRef('AppSyncAuthentication'), NoneType] = None, ssl: Union[ssl.SSLContext, bool, aiohttp.client_reqrep.Fingerprint, str] = 'ssl_warning', timeout: Optional[int] = None, ssl_close_timeout: Union[int, float, NoneType] = 10, json_serialize: Callable = <function dumps at 0x00000260033BBE20>, client_session_args: Optional[Dict[str, Any]] = None) -> None`

:ref:`Async Transport <async_transports>` to execute GraphQL queries
on remote servers with an HTTP connection.

This transport use the aiohttp library with asyncio.

### `Client(self, schema: Union[str, graphql.type.schema.GraphQLSchema, NoneType] = None, introspection: Optional[graphql.utilities.get_introspection_query.IntrospectionQuery] = None, transport: Union[gql.transport.transport.Transport, gql.transport.async_transport.AsyncTransport, NoneType] = None, fetch_schema_from_transport: bool = False, introspection_args: Optional[Dict] = None, execute_timeout: Union[int, float, NoneType] = 10, serialize_variables: bool = False, parse_results: bool = False, batch_interval: float = 0, batch_max: int = 10)`

The Client class is the main entrypoint to execute GraphQL requests
on a GQL transport.

It can take sync or async transports as argument and can either execute
and subscribe to requests itself with the
:func:`execute <gql.client.Client.execute>` and
:func:`subscribe <gql.client.Client.subscribe>` methods
OR can be used to get a sync or async session depending on the
transport type.

To connect to an :ref:`async transport <async_transports>` and get an
:class:`async session <gql.client.AsyncClientSession>`,
use :code:`async with client as session:`

To connect to a :ref:`sync transport <sync_transports>` and get a
:class:`sync session <gql.client.SyncClientSession>`,
use :code:`with client as session:`

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created due to permissions or other issues.

### `gql(request_string: 'str | Source') -> 'DocumentNode'`

Given a string containing a GraphQL request, parse it into a Document.

:param request_string: the GraphQL request as a String
:type request_string: str | Source
:return: a Document which can be later executed or subscribed by a
    :class:`Client <gql.client.Client>`, by an
    :class:`async session <gql.client.AsyncClientSession>` or by a
    :class:`sync session <gql.client.SyncClientSession>`

:raises GraphQLError: if a syntax error is encountered.

### `run(storage_path: str | pathlib.Path, config: dict, api_key: str) -> dict | str`

Main entry point for the schema monitoring agent.

Args:
    storage_path (str | Path): Daily storage path.
    config (dict): Loaded YAML configuration.
    api_key (str): OpenStates API key.

Returns:
    dict or str: Parsed schema or access message.
