import inspect
from functools import wraps
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from pait.app.base import BaseSyncAppHelper, BaseAsyncAppHelper
from pait.g import pait_data
from pait.model import PaitCoreModel, PaitResponseModel, PaitStatus
from pait.param_handle import async_class_param_handle, async_func_param_handle, class_param_handle, func_param_handle
from pait.util import get_func_sig, FuncSig


def pait(
    app_helper_class: "Type[Union[BaseSyncAppHelper, BaseAsyncAppHelper]]",
    author: Optional[Tuple[str]] = None,
    desc: Optional[str] = None,
    status: Optional[PaitStatus] = None,
    group: Optional[str] = None,
    tag: Optional[Tuple[str, ...]] = None,
    response_model_list: Optional[List[Type[PaitResponseModel]]] = None,
) -> Callable:
    if not isinstance(app_helper_class, type):
        raise TypeError(f"{app_helper_class} must be class")

    def wrapper(func: Callable) -> Callable:
        func_sig: FuncSig = get_func_sig(func)
        qualname = func.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]

        pait_id: str = f"{qualname}_{id(func)}"
        setattr(func, "_pait_id", pait_id)
        pait_data.register(
            PaitCoreModel(
                author=author,
                desc=desc,
                func=func,
                pait_id=pait_id,
                status=status,
                group=group,
                tag=tag,
                response_model_list=response_model_list,
            )
        )

        if inspect.iscoroutinefunction(func) and issubclass(app_helper_class, BaseAsyncAppHelper):

            @wraps(func)
            async def dispatch(*args: Any, **kwargs: Any) -> Callable:
                # only use in runtime, support cbv
                class_ = getattr(inspect.getmodule(func), qualname)
                # real param handle
                app_helper: BaseAsyncAppHelper = app_helper_class(class_, args, kwargs)  # type: ignore
                # auto gen param from request
                func_args, func_kwargs = await async_func_param_handle(app_helper, func_sig)
                # support sbv
                await async_class_param_handle(app_helper)
                return await func(*func_args, **func_kwargs)

            return dispatch
        elif issubclass(app_helper_class, BaseSyncAppHelper):

            @wraps(func)
            def dispatch(*args: Any, **kwargs: Any) -> Callable:
                # only use in runtime
                class_ = getattr(inspect.getmodule(func), qualname)
                # real param handle
                app_helper: BaseSyncAppHelper = app_helper_class(class_, args, kwargs)  # type: ignore
                # auto gen param from request
                func_args, func_kwargs = func_param_handle(app_helper, func_sig)
                # support sbv
                class_param_handle(app_helper)
                return func(*func_args, **func_kwargs)

            return dispatch
        else:
            raise RuntimeError("Please check pait app helper or func")

    return wrapper
