from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("guides", sa.Column("bio", sa.Text(), nullable=True))
    op.add_column("guides", sa.Column("specialties", sa.String(300), nullable=True))
    op.add_column("guides", sa.Column("regions", sa.String(300), nullable=True))
    op.add_column("guides", sa.Column("hourly_rate", sa.Numeric(10, 2), nullable=True))
    op.add_column("guides", sa.Column("daily_rate", sa.Numeric(10, 2), nullable=True))
    op.add_column("guides", sa.Column("is_available", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.add_column("guides", sa.Column("photo_url", sa.String(500), nullable=True))
    op.add_column("guides", sa.Column("whatsapp", sa.String(30), nullable=True))
    op.add_column("guides", sa.Column("facebook", sa.String(200), nullable=True))
    op.add_column("guides", sa.Column("instagram", sa.String(200), nullable=True))
    op.add_column("guides", sa.Column("total_reviews", sa.Integer(), server_default=sa.text("0"), nullable=False))
    op.add_column("guides", sa.Column("avg_rating", sa.Numeric(2, 1), nullable=True))


def downgrade() -> None:
    op.drop_column("guides", "avg_rating")
    op.drop_column("guides", "total_reviews")
    op.drop_column("guides", "instagram")
    op.drop_column("guides", "facebook")
    op.drop_column("guides", "whatsapp")
    op.drop_column("guides", "photo_url")
    op.drop_column("guides", "is_available")
    op.drop_column("guides", "daily_rate")
    op.drop_column("guides", "hourly_rate")
    op.drop_column("guides", "regions")
    op.drop_column("guides", "specialties")
    op.drop_column("guides", "bio")
