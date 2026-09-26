"""init - butun cedvelleri yaradir

Revision ID: 0001_init
Revises:
Create Date: 2026-09-26

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Modellərdən (app/db/models.py) bütün cədvəlləri birbaşa yaradırıq —
    # beləcə sxem həmişə models.py ilə tam üst-üstə düşür.
    from app.db.database import Base
    from app.db import models  # noqa: F401 (modellər Base.metadata-ya qeydiyyatdan keçsin deyə import olunur)

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    from app.db.database import Base
    from app.db import models  # noqa: F401

    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
