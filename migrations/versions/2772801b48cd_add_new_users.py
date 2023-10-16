"""add_new_users

Revision ID: 2772801b48cd
Revises: 83c749764db8
Create Date: 2023-10-16 00:51:24.076473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from casestudy.database.models import User



# revision identifiers, used by Alembic.
revision = '2772801b48cd'
down_revision = '83c749764db8'
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
