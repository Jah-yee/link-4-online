import asyncio
from collections.abc import Callable
from typing import Any
import inspect
import logging

logger = logging.getLogger("uvicorn.error")

class Debounce:
    def __init__(
        self,
        debounce_time_ms: int,
        callback: Callable[[], Any],
        *args: Any,
        **kwargs: dict[str, Any],
    ):
        self._debounce_time_scound: int = debounce_time_ms
        logger.info(
            f"create Debounce time:{self._debounce_time_scound}  {inspect.iscoroutinefunction(callback)}"
        )
        self._calllback: Callable[[], Any] = callback
        self._calllback_args: Any = args
        self._callback_kwargs: dict[str, Any] = kwargs
        self._task: asyncio.Task[Any] | None = None
        self._is_coroutine_function = inspect.iscoroutinefunction(self._calllback)
        self.setTimer()

    def setTimer(self):
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = asyncio.create_task(self._run_calllback())

    def resetTimer(self):
        logger.info("resetTimer")
        self.setTimer()

    async def _run_calllback(self):
        try:
            await asyncio.sleep(self._debounce_time_scound)
            logger.info("Debounce run calllback")
            if self._is_coroutine_function:
                await self._calllback(*self._calllback_args, **self._callback_kwargs)
            else:
                await asyncio.to_thread(
                    self._calllback, *self._calllback_args, *self._callback_kwargs
                )
        except asyncio.CancelledError:
            pass
