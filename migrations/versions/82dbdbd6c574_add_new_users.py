"""add new users

Revision ID: 82dbdbd6c574
Revises: fc811be01ebe
Create Date: 2023-10-15 23:57:04.225356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from casestudy.database.models import User  # Import your User model


# revision identifiers, used by Alembic.
revision = '82dbdbd6c574'
down_revision = 'fc811be01ebe'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    Session = sessionmaker(bind=bind)
    session = Session()
    user1 = User(username='user1', first_name='john', last_name='smith')
    user2 = User(username='user2', first_name='jane', last_name='doe')

    session.add(user1)
    session.add(user2)
    session.commit()

def downgrade():
    pass
