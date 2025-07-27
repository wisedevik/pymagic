from sqlalchemy.future import select
from server.database.models import Account
from server.database import AsyncSessionLocal
from sqlalchemy.future import select


class AccountCrud:
    async def get_account_by_token(token: str | None):
        if token is None:
            return None

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Account).where(Account.pass_token == token)
            )
            return result.scalar_one_or_none()

    async def create_account(token: str):
        async with AsyncSessionLocal() as session:
            account = Account(pass_token=token)
            session.add(account)
            await session.commit()
            await session.refresh(account)
            return account
