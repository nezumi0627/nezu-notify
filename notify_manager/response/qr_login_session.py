from pydantic import BaseModel


class QRLoginSessionResponse(BaseModel):
    qrCodePath: str

    @property
    def code(self) -> str:
        return self.qrCodePath.split("/")[-1]
