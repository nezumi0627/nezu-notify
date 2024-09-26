import sys
from threading import Event, Thread
from time import sleep
from typing import Any

from pydantic import BaseModel, Field


class Countdown(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    seconds: int
    message: str = Field(default="countdown")
    event: Event = Field(init=False, default_factory=Event)
    thread: Thread = Field(init=False, default_factory=Thread)

    def model_post_init(self, __context: Any) -> None:
        self.event = Event()
        self.thread = Thread(target=self._run)

    def _run(self) -> None:
        for i in range(self.seconds, 0, -1):
            if self.event.is_set():
                print()
                return
            hours, remainder = divmod(i, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_format = f"{hours:02}:{minutes:02}:{seconds:02}"

            sys.stdout.write(f"\r{self.message}: {time_format}")
            sys.stdout.flush()
            sleep(1)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.event.set()
        self.thread.join()
