from sqlalchemy import select

from src.models.user import User


async def test_when_create_user_in_database_Return_success(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'