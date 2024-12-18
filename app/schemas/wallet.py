from pydantic import BaseModel


class GeneratedWalletResponse(BaseModel):
    address: str


class GeneratedWalletFullData(GeneratedWalletResponse):
    private_key: str
    public_key: str
