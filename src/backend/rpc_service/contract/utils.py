import inspect
from typing import Callable, Any, Type
import pydantic
from ..messages import RequestMessage


def build_request_message_type(func: Callable[..., Any]) -> Type[RequestMessage]:
    """
    Генерирует pydantic модель, соответствующую сигнатуре переданной функции.

    :param func: функция, на основе сигнатуры которой генерируется модель
    :return: сгенерированная модель запроса
    """

    fields = dict()

    for name, info in inspect.signature(func).parameters.items():
        if name in ("self", "cls"):
            continue

        annotation = info.annotation if info.annotation != inspect.Signature.empty else Any
        default = info.default if info.default != inspect.Signature.empty else ...

        fields[name] = (annotation, default)

    return pydantic.create_model(
        __model_name=f"{func.__name__}_request",
        __base__=RequestMessage,
        **fields)
