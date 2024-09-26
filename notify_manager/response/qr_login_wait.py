from typing import Optional

from notify_manager.response._base_wait import BaseWaitResponse


class QRLoginWaitResponse(BaseWaitResponse):
    pinCode: Optional[str]
