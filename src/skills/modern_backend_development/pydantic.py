"""
Auto-generated skill for pydantic

This skill wraps the public API of the pydantic library.
Generated on: 2026-03-20T19:13:03.456223
Library version: 2.12.5

Wrapped components: 147

Usage:
    Invoke without action to list available wrappers:
        await invoke({"action": None})
    
    Invoke a specific wrapper:
        await invoke({"action": "function_name", "args": [arg1, arg2], "kwargs": {"key": "value"}})
"""
import inspect
import logging
from typing import Any, Dict, List

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WRAPPED_NAMES = ["AfterValidator", "AliasChoices", "AliasGenerator", "AliasPath", "AllowInfNan", "AmqpDsn", "AnyHttpUrl", "AnyUrl", "AnyWebsocketUrl", "AwareDatetime", "Base64Bytes", "Base64Encoder", "Base64Str", "Base64UrlBytes", "Base64UrlStr", "BaseConfig", "BaseModel", "BeforeValidator", "ByteSize", "ClickHouseDsn", "CockroachDsn", "ConfigDict", "DirectoryPath", "Discriminator", "EmailStr", "EncodedBytes", "EncodedStr", "EncoderProtocol", "Extra", "FailFast", "Field", "FieldSerializationInfo", "FilePath", "FileUrl", "FiniteFloat", "FtpUrl", "FutureDate", "FutureDatetime", "GetCoreSchemaHandler", "GetJsonSchemaHandler", "GetPydanticSchema", "HttpUrl", "IPvAnyAddress", "IPvAnyInterface", "IPvAnyNetwork", "ImportString", "InstanceOf", "Json", "KafkaDsn", "MariaDBDsn", "ModelWrapValidatorHandler", "MongoDsn", "MySQLDsn", "NaiveDatetime", "NameEmail", "NatsDsn", "NegativeFloat", "NegativeInt", "NewPath", "NonNegativeFloat", "NonNegativeInt", "NonPositiveFloat", "NonPositiveInt", "OnErrorOmit", "PastDate", "PastDatetime", "PaymentCardNumber", "PlainSerializer", "PlainValidator", "PositiveFloat", "PositiveInt", "PostgresDsn", "PrivateAttr", "PydanticDeprecatedSince20", "PydanticDeprecatedSince210", "PydanticDeprecatedSince211", "PydanticDeprecatedSince212", "PydanticDeprecatedSince26", "PydanticDeprecatedSince29", "PydanticDeprecationWarning", "PydanticErrorCodes", "PydanticExperimentalWarning", "PydanticForbiddenQualifier", "PydanticImportError", "PydanticInvalidForJsonSchema", "PydanticSchemaGenerationError", "PydanticUndefinedAnnotation", "PydanticUserError", "RedisDsn", "RootModel", "Secret", "SecretBytes", "SecretStr", "SerializationInfo", "SerializeAsAny", "SerializerFunctionWrapHandler", "SkipValidation", "SnowflakeDsn", "SocketPath", "Strict", "StrictBool", "StrictBytes", "StrictFloat", "StrictInt", "StrictStr", "StringConstraints", "Tag", "TypeAdapter", "UUID1", "UUID3", "UUID4", "UUID5", "UUID6", "UUID7", "UUID8", "UrlConstraints", "ValidateAs", "ValidationError", "ValidationInfo", "ValidatorFunctionWrapHandler", "WebsocketUrl", "WithJsonSchema", "WrapSerializer", "WrapValidator", "computed_field", "conbytes", "condate", "condecimal", "confloat", "confrozenset", "conint", "conlist", "conset", "constr", "create_model", "field_serializer", "field_validator", "model_serializer", "model_validator", "parse_obj_as", "root_validator", "schema_json_of", "schema_of", "validate_call", "validate_email", "validator", "with_config"]

async def AfterValidator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AfterValidator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AfterValidator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AliasChoices_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AliasChoices
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AliasChoices")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AliasGenerator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AliasGenerator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AliasGenerator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AliasPath_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AliasPath
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AliasPath")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AllowInfNan_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AllowInfNan
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AllowInfNan")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AmqpDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AmqpDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AmqpDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AnyHttpUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AnyHttpUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AnyHttpUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AnyUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AnyUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AnyUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AnyWebsocketUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AnyWebsocketUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AnyWebsocketUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def AwareDatetime_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.AwareDatetime
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "AwareDatetime")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Base64Bytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Base64Bytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Base64Bytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Base64Encoder_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Base64Encoder
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Base64Encoder")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Base64Str_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Base64Str
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Base64Str")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Base64UrlBytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Base64UrlBytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Base64UrlBytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Base64UrlStr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Base64UrlStr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Base64UrlStr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def BaseConfig_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.BaseConfig
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "BaseConfig")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def BaseModel_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.BaseModel
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "BaseModel")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def BeforeValidator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.BeforeValidator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "BeforeValidator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ByteSize_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ByteSize
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ByteSize")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ClickHouseDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ClickHouseDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ClickHouseDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def CockroachDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.CockroachDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "CockroachDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ConfigDict_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ConfigDict
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ConfigDict")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def DirectoryPath_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.DirectoryPath
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "DirectoryPath")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Discriminator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Discriminator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Discriminator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def EmailStr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.EmailStr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "EmailStr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def EncodedBytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.EncodedBytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "EncodedBytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def EncodedStr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.EncodedStr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "EncodedStr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def EncoderProtocol_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.EncoderProtocol
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "EncoderProtocol")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Extra_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Extra
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Extra")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FailFast_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FailFast
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FailFast")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Field_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Field
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Field")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FieldSerializationInfo_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FieldSerializationInfo
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FieldSerializationInfo")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FilePath_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FilePath
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FilePath")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FileUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FileUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FileUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FiniteFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FiniteFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FiniteFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FtpUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FtpUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FtpUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FutureDate_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FutureDate
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FutureDate")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FutureDatetime_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.FutureDatetime
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "FutureDatetime")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def GetCoreSchemaHandler_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.GetCoreSchemaHandler
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "GetCoreSchemaHandler")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def GetJsonSchemaHandler_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.GetJsonSchemaHandler
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "GetJsonSchemaHandler")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def GetPydanticSchema_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.GetPydanticSchema
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "GetPydanticSchema")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def HttpUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.HttpUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "HttpUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def IPvAnyAddress_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.IPvAnyAddress
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "IPvAnyAddress")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def IPvAnyInterface_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.IPvAnyInterface
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "IPvAnyInterface")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def IPvAnyNetwork_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.IPvAnyNetwork
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "IPvAnyNetwork")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ImportString_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ImportString
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ImportString")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def InstanceOf_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.InstanceOf
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "InstanceOf")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Json_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Json
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Json")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def KafkaDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.KafkaDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "KafkaDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def MariaDBDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.MariaDBDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "MariaDBDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ModelWrapValidatorHandler_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ModelWrapValidatorHandler
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ModelWrapValidatorHandler")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def MongoDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.MongoDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "MongoDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def MySQLDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.MySQLDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "MySQLDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NaiveDatetime_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NaiveDatetime
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NaiveDatetime")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NameEmail_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NameEmail
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NameEmail")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NatsDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NatsDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NatsDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NegativeFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NegativeFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NegativeFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NegativeInt_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NegativeInt
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NegativeInt")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NewPath_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NewPath
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NewPath")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NonNegativeFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NonNegativeFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NonNegativeFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NonNegativeInt_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NonNegativeInt
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NonNegativeInt")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NonPositiveFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NonPositiveFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NonPositiveFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def NonPositiveInt_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.NonPositiveInt
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "NonPositiveInt")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def OnErrorOmit_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.OnErrorOmit
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "OnErrorOmit")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PastDate_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PastDate
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PastDate")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PastDatetime_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PastDatetime
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PastDatetime")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PaymentCardNumber_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PaymentCardNumber
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PaymentCardNumber")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PlainSerializer_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PlainSerializer
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PlainSerializer")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PlainValidator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PlainValidator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PlainValidator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PositiveFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PositiveFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PositiveFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PositiveInt_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PositiveInt
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PositiveInt")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PostgresDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PostgresDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PostgresDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PrivateAttr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PrivateAttr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PrivateAttr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince20_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince20
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince20")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince210_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince210
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince210")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince211_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince211
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince211")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince212_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince212
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince212")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince26_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince26
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince26")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecatedSince29_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecatedSince29
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecatedSince29")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticDeprecationWarning_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticDeprecationWarning
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticDeprecationWarning")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticErrorCodes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticErrorCodes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticErrorCodes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticExperimentalWarning_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticExperimentalWarning
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticExperimentalWarning")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticForbiddenQualifier_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticForbiddenQualifier
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticForbiddenQualifier")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticImportError_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticImportError
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticImportError")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticInvalidForJsonSchema_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticInvalidForJsonSchema
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticInvalidForJsonSchema")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticSchemaGenerationError_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticSchemaGenerationError
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticSchemaGenerationError")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticUndefinedAnnotation_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticUndefinedAnnotation
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticUndefinedAnnotation")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def PydanticUserError_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.PydanticUserError
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "PydanticUserError")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def RedisDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.RedisDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "RedisDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def RootModel_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.RootModel
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "RootModel")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Secret_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Secret
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Secret")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SecretBytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SecretBytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SecretBytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SecretStr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SecretStr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SecretStr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SerializationInfo_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SerializationInfo
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SerializationInfo")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SerializeAsAny_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SerializeAsAny
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SerializeAsAny")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SerializerFunctionWrapHandler_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SerializerFunctionWrapHandler
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SerializerFunctionWrapHandler")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SkipValidation_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SkipValidation
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SkipValidation")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SnowflakeDsn_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SnowflakeDsn
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SnowflakeDsn")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def SocketPath_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.SocketPath
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "SocketPath")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Strict_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Strict
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Strict")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StrictBool_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StrictBool
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StrictBool")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StrictBytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StrictBytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StrictBytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StrictFloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StrictFloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StrictFloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StrictInt_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StrictInt
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StrictInt")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StrictStr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StrictStr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StrictStr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def StringConstraints_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.StringConstraints
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "StringConstraints")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Tag_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.Tag
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "Tag")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def TypeAdapter_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.TypeAdapter
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "TypeAdapter")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID1_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID1
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID1")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID3_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID3
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID3")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID4_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID4
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID4")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID5_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID5
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID5")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID6_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID6
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID6")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID7_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID7
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID7")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UUID8_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UUID8
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UUID8")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UrlConstraints_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.UrlConstraints
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "UrlConstraints")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ValidateAs_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ValidateAs
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ValidateAs")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ValidationError_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ValidationError
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ValidationError")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ValidationInfo_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ValidationInfo
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ValidationInfo")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def ValidatorFunctionWrapHandler_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.ValidatorFunctionWrapHandler
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "ValidatorFunctionWrapHandler")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WebsocketUrl_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.WebsocketUrl
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "WebsocketUrl")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WithJsonSchema_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.WithJsonSchema
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "WithJsonSchema")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WrapSerializer_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.WrapSerializer
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "WrapSerializer")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WrapValidator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.WrapValidator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "WrapValidator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def computed_field_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.computed_field
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "computed_field")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def conbytes_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.conbytes
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "conbytes")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def condate_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.condate
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "condate")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def condecimal_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.condecimal
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "condecimal")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def confloat_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.confloat
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "confloat")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def confrozenset_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.confrozenset
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "confrozenset")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def conint_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.conint
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "conint")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def conlist_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.conlist
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "conlist")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def conset_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.conset
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "conset")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def constr_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.constr
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "constr")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def create_model_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.create_model
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "create_model")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def field_serializer_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.field_serializer
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "field_serializer")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def field_validator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.field_validator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "field_validator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def model_serializer_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.model_serializer
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "model_serializer")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def model_validator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.model_validator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "model_validator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def parse_obj_as_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.parse_obj_as
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "parse_obj_as")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def root_validator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.root_validator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "root_validator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def schema_json_of_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.schema_json_of
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "schema_json_of")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def schema_of_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.schema_of
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "schema_of")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def validate_call_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.validate_call
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "validate_call")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def validate_email_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.validate_email
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "validate_email")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def validator_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.validator
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "validator")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def with_config_wrapper(args: list, kwargs: dict):
    """
    Wrapper for pydantic.with_config
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import pydantic
        member = getattr(pydantic, "with_config")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for skill invocation.
    
    Expected payload:
        - action: str (optional): Name of wrapper to call. If omitted, returns list of available wrappers
        - args: list (optional): Positional arguments for the wrapper
        - kwargs: dict (optional): Keyword arguments for the wrapper
    
    Returns:
        dict with 'result' and 'metadata' keys
    """
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action")
    args = payload.get("args", [])
    kwargs = payload.get("kwargs", {})
    
    if action is None:
        return {
            "result": {
                "available_wrappers": list(WRAPPED_NAMES),
                "message": "Available wrappers. Use action parameter to call a specific wrapper."
            },
            "metadata": {
                "timestamp": timestamp,
                "library": "pydantic",
                "function_count": len(WRAPPED_NAMES)
            }
        }
    
    if action not in WRAPPED_NAMES:
        return {
            "result": {"error": "Unknown action: " + action},
            "metadata": {
                "timestamp": timestamp,
                "error": "Action not found in wrapped names"
            }
        }
    
    wrappers = {
        "AfterValidator": AfterValidator_wrapper,
        "AliasChoices": AliasChoices_wrapper,
        "AliasGenerator": AliasGenerator_wrapper,
        "AliasPath": AliasPath_wrapper,
        "AllowInfNan": AllowInfNan_wrapper,
        "AmqpDsn": AmqpDsn_wrapper,
        "AnyHttpUrl": AnyHttpUrl_wrapper,
        "AnyUrl": AnyUrl_wrapper,
        "AnyWebsocketUrl": AnyWebsocketUrl_wrapper,
        "AwareDatetime": AwareDatetime_wrapper,
        "Base64Bytes": Base64Bytes_wrapper,
        "Base64Encoder": Base64Encoder_wrapper,
        "Base64Str": Base64Str_wrapper,
        "Base64UrlBytes": Base64UrlBytes_wrapper,
        "Base64UrlStr": Base64UrlStr_wrapper,
        "BaseConfig": BaseConfig_wrapper,
        "BaseModel": BaseModel_wrapper,
        "BeforeValidator": BeforeValidator_wrapper,
        "ByteSize": ByteSize_wrapper,
        "ClickHouseDsn": ClickHouseDsn_wrapper,
        "CockroachDsn": CockroachDsn_wrapper,
        "ConfigDict": ConfigDict_wrapper,
        "DirectoryPath": DirectoryPath_wrapper,
        "Discriminator": Discriminator_wrapper,
        "EmailStr": EmailStr_wrapper,
        "EncodedBytes": EncodedBytes_wrapper,
        "EncodedStr": EncodedStr_wrapper,
        "EncoderProtocol": EncoderProtocol_wrapper,
        "Extra": Extra_wrapper,
        "FailFast": FailFast_wrapper,
        "Field": Field_wrapper,
        "FieldSerializationInfo": FieldSerializationInfo_wrapper,
        "FilePath": FilePath_wrapper,
        "FileUrl": FileUrl_wrapper,
        "FiniteFloat": FiniteFloat_wrapper,
        "FtpUrl": FtpUrl_wrapper,
        "FutureDate": FutureDate_wrapper,
        "FutureDatetime": FutureDatetime_wrapper,
        "GetCoreSchemaHandler": GetCoreSchemaHandler_wrapper,
        "GetJsonSchemaHandler": GetJsonSchemaHandler_wrapper,
        "GetPydanticSchema": GetPydanticSchema_wrapper,
        "HttpUrl": HttpUrl_wrapper,
        "IPvAnyAddress": IPvAnyAddress_wrapper,
        "IPvAnyInterface": IPvAnyInterface_wrapper,
        "IPvAnyNetwork": IPvAnyNetwork_wrapper,
        "ImportString": ImportString_wrapper,
        "InstanceOf": InstanceOf_wrapper,
        "Json": Json_wrapper,
        "KafkaDsn": KafkaDsn_wrapper,
        "MariaDBDsn": MariaDBDsn_wrapper,
        "ModelWrapValidatorHandler": ModelWrapValidatorHandler_wrapper,
        "MongoDsn": MongoDsn_wrapper,
        "MySQLDsn": MySQLDsn_wrapper,
        "NaiveDatetime": NaiveDatetime_wrapper,
        "NameEmail": NameEmail_wrapper,
        "NatsDsn": NatsDsn_wrapper,
        "NegativeFloat": NegativeFloat_wrapper,
        "NegativeInt": NegativeInt_wrapper,
        "NewPath": NewPath_wrapper,
        "NonNegativeFloat": NonNegativeFloat_wrapper,
        "NonNegativeInt": NonNegativeInt_wrapper,
        "NonPositiveFloat": NonPositiveFloat_wrapper,
        "NonPositiveInt": NonPositiveInt_wrapper,
        "OnErrorOmit": OnErrorOmit_wrapper,
        "PastDate": PastDate_wrapper,
        "PastDatetime": PastDatetime_wrapper,
        "PaymentCardNumber": PaymentCardNumber_wrapper,
        "PlainSerializer": PlainSerializer_wrapper,
        "PlainValidator": PlainValidator_wrapper,
        "PositiveFloat": PositiveFloat_wrapper,
        "PositiveInt": PositiveInt_wrapper,
        "PostgresDsn": PostgresDsn_wrapper,
        "PrivateAttr": PrivateAttr_wrapper,
        "PydanticDeprecatedSince20": PydanticDeprecatedSince20_wrapper,
        "PydanticDeprecatedSince210": PydanticDeprecatedSince210_wrapper,
        "PydanticDeprecatedSince211": PydanticDeprecatedSince211_wrapper,
        "PydanticDeprecatedSince212": PydanticDeprecatedSince212_wrapper,
        "PydanticDeprecatedSince26": PydanticDeprecatedSince26_wrapper,
        "PydanticDeprecatedSince29": PydanticDeprecatedSince29_wrapper,
        "PydanticDeprecationWarning": PydanticDeprecationWarning_wrapper,
        "PydanticErrorCodes": PydanticErrorCodes_wrapper,
        "PydanticExperimentalWarning": PydanticExperimentalWarning_wrapper,
        "PydanticForbiddenQualifier": PydanticForbiddenQualifier_wrapper,
        "PydanticImportError": PydanticImportError_wrapper,
        "PydanticInvalidForJsonSchema": PydanticInvalidForJsonSchema_wrapper,
        "PydanticSchemaGenerationError": PydanticSchemaGenerationError_wrapper,
        "PydanticUndefinedAnnotation": PydanticUndefinedAnnotation_wrapper,
        "PydanticUserError": PydanticUserError_wrapper,
        "RedisDsn": RedisDsn_wrapper,
        "RootModel": RootModel_wrapper,
        "Secret": Secret_wrapper,
        "SecretBytes": SecretBytes_wrapper,
        "SecretStr": SecretStr_wrapper,
        "SerializationInfo": SerializationInfo_wrapper,
        "SerializeAsAny": SerializeAsAny_wrapper,
        "SerializerFunctionWrapHandler": SerializerFunctionWrapHandler_wrapper,
        "SkipValidation": SkipValidation_wrapper,
        "SnowflakeDsn": SnowflakeDsn_wrapper,
        "SocketPath": SocketPath_wrapper,
        "Strict": Strict_wrapper,
        "StrictBool": StrictBool_wrapper,
        "StrictBytes": StrictBytes_wrapper,
        "StrictFloat": StrictFloat_wrapper,
        "StrictInt": StrictInt_wrapper,
        "StrictStr": StrictStr_wrapper,
        "StringConstraints": StringConstraints_wrapper,
        "Tag": Tag_wrapper,
        "TypeAdapter": TypeAdapter_wrapper,
        "UUID1": UUID1_wrapper,
        "UUID3": UUID3_wrapper,
        "UUID4": UUID4_wrapper,
        "UUID5": UUID5_wrapper,
        "UUID6": UUID6_wrapper,
        "UUID7": UUID7_wrapper,
        "UUID8": UUID8_wrapper,
        "UrlConstraints": UrlConstraints_wrapper,
        "ValidateAs": ValidateAs_wrapper,
        "ValidationError": ValidationError_wrapper,
        "ValidationInfo": ValidationInfo_wrapper,
        "ValidatorFunctionWrapHandler": ValidatorFunctionWrapHandler_wrapper,
        "WebsocketUrl": WebsocketUrl_wrapper,
        "WithJsonSchema": WithJsonSchema_wrapper,
        "WrapSerializer": WrapSerializer_wrapper,
        "WrapValidator": WrapValidator_wrapper,
        "computed_field": computed_field_wrapper,
        "conbytes": conbytes_wrapper,
        "condate": condate_wrapper,
        "condecimal": condecimal_wrapper,
        "confloat": confloat_wrapper,
        "confrozenset": confrozenset_wrapper,
        "conint": conint_wrapper,
        "conlist": conlist_wrapper,
        "conset": conset_wrapper,
        "constr": constr_wrapper,
        "create_model": create_model_wrapper,
        "field_serializer": field_serializer_wrapper,
        "field_validator": field_validator_wrapper,
        "model_serializer": model_serializer_wrapper,
        "model_validator": model_validator_wrapper,
        "parse_obj_as": parse_obj_as_wrapper,
        "root_validator": root_validator_wrapper,
        "schema_json_of": schema_json_of_wrapper,
        "schema_of": schema_of_wrapper,
        "validate_call": validate_call_wrapper,
        "validate_email": validate_email_wrapper,
        "validator": validator_wrapper,
        "with_config": with_config_wrapper,
    }
    
    try:
        result = await wrappers[action](args, kwargs)
        elapsed = time.time() - start_time
        
        return {
            "result": result,
            "metadata": {
                "timestamp": timestamp,
                "library": "pydantic",
                "library_version": "2.12.5" if "2.12.5" != "None" else None,
                "action": action,
                "elapsed_seconds": elapsed
            }
        }
    except Exception as e:
        logger.error("Error invoking {}: {}".format(action, str(e)))
        return {
            "result": {"error": str(e)},
            "metadata": {
                "timestamp": timestamp,
                "library": "pydantic",
                "error": str(e)
            }
        }


def register_skill():
    """Return skill metadata for registration"""
    return {
        "name": "pydantic-wrapper",
        "description": "Auto-generated skill wrapping pydantic public API",
        "domain": "modern_backend_development",
        "version": "1.0.0",
    }
