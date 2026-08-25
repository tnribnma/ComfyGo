from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("hotels", sa.Column("price_per_night", sa.Numeric(10, 2), nullable=True))
    op.add_column("hotels", sa.Column("breakfast_included", sa.Boolean(), server_default=sa.text("false"), nullable=False))
    op.add_column("hotels", sa.Column("free_cancellation", sa.Boolean(), server_default=sa.text("false"), nullable=False))
    op.add_column("hotels", sa.Column("has_pool", sa.Boolean(), server_default=sa.text("false"), nullable=False))
    op.add_column("hotels", sa.Column("has_wifi", sa.Boolean(), server_default=sa.text("false"), nullable=False))
    op.add_column("hotels", sa.Column("has_parking", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    op.drop_column("hotels", "has_parking")
    op.drop_column("hotels", "has_wifi")
    op.drop_column("hotels", "has_pool")
    op.drop_column("hotels", "free_cancellation")
    op.drop_column("hotels", "breakfast_included")
    op.drop_column("hotels", "price_per_night")
