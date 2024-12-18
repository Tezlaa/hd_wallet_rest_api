from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
auto_now_dt = Annotated[datetime, mapped_column(server_default=text("Timezone('UTC', now())"))]
unique_str = Annotated[str, mapped_column(unique=True)]
unique_int = Annotated[int, mapped_column(unique=True)]
