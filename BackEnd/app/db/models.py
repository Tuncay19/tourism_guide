import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column, String, Boolean, Float, Integer, DateTime, ForeignKey, Enum,
    UniqueConstraint, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


def gen_uuid():
    return str(uuid.uuid4())


def utcnow():
    return datetime.now(timezone.utc)


class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class AuthProviderEnum(str, enum.Enum):
    LOCAL = "LOCAL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"


# -------------------------------
# İSTİFADƏÇİLƏR VƏ AUTENTİFİKASİYA
# -------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)  # LOCAL qeydiyyat üçün (bcrypt hash)
    full_name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    is_verified = Column(Boolean, default=False)

    # Şəxsi seçimlər — fərdi tur tövsiyəsi üçün
    interests = Column(ARRAY(String), default=list)  # məs: ["tarix", "təbiət", "qastronomiya"]
    budget_level = Column(String, nullable=True)      # "low" | "medium" | "high"
    travel_style = Column(String, nullable=True)       # "solo" | "family" | "couple" | "group"

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    tour_plans = relationship("TourPlan", back_populates="user", cascade="all, delete-orphan")


class Account(Base):
    """Google/Facebook kimi sosial hesabları User-ə bağlamaq üçün."""
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("provider", "provider_account_id", name="uq_provider_account"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    provider = Column(Enum(AuthProviderEnum), nullable=False)
    provider_account_id = Column(String, nullable=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow)

    user = relationship("User", back_populates="accounts")


# -------------------------------
# KATEQORİYALAR
# -------------------------------

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, unique=True, nullable=False)  # "Tarixi abidə", "Təbiət", "Muzey"...
    icon = Column(String, nullable=True)

    places = relationship("Place", back_populates="category")
    restaurants = relationship("Restaurant", back_populates="category")


# -------------------------------
# MƏKANLAR
# -------------------------------

class Place(Base):
    __tablename__ = "places"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    region = Column(String, nullable=False)  # "Şuşa", "Xankəndi", "Ağdam", "Füzuli"...
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    images = Column(ARRAY(String), default=list)

    category_id = Column(UUID(as_uuid=False), ForeignKey("categories.id"), nullable=True)

    avg_rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    category = relationship("Category", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="place", cascade="all, delete-orphan")
    tour_items = relationship("TourPlanItem", back_populates="place")


# -------------------------------
# RESTORANLAR
# -------------------------------

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    region = Column(String, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    images = Column(ARRAY(String), default=list)
    cuisine_type = Column(String, nullable=True)   # "Azərbaycan", "Avropa", "Fast-food"...
    price_range = Column(String, nullable=True)     # "$" | "$$" | "$$$"
    opening_hours = Column(String, nullable=True)

    category_id = Column(UUID(as_uuid=False), ForeignKey("categories.id"), nullable=True)

    avg_rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    category = relationship("Category", back_populates="restaurants")
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="restaurant", cascade="all, delete-orphan")
    tour_items = relationship("TourPlanItem", back_populates="restaurant")


# -------------------------------
# RƏYLƏR
# -------------------------------

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(UUID(as_uuid=False), ForeignKey("places.id", ondelete="CASCADE"), nullable=True)
    restaurant_id = Column(UUID(as_uuid=False), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=True)

    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow)

    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")


# -------------------------------
# FAVORİTLƏR
# -------------------------------

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "place_id", "restaurant_id", name="uq_user_favorite"),
    )

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(UUID(as_uuid=False), ForeignKey("places.id", ondelete="CASCADE"), nullable=True)
    restaurant_id = Column(UUID(as_uuid=False), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow)

    user = relationship("User", back_populates="favorites")
    place = relationship("Place", back_populates="favorites")
    restaurant = relationship("Restaurant", back_populates="favorites")


# -------------------------------
# FƏRDİ TUR PLANLARI
# -------------------------------

class TourPlan(Base):
    __tablename__ = "tour_plans"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="tour_plans")
    items = relationship("TourPlanItem", back_populates="tour_plan", cascade="all, delete-orphan")


class TourPlanItem(Base):
    __tablename__ = "tour_plan_items"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    tour_plan_id = Column(UUID(as_uuid=False), ForeignKey("tour_plans.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(UUID(as_uuid=False), ForeignKey("places.id"), nullable=True)
    restaurant_id = Column(UUID(as_uuid=False), ForeignKey("restaurants.id"), nullable=True)

    day_number = Column(Integer, nullable=False)   # Turun neçənci günü
    order_index = Column(Integer, nullable=False)  # O gün daxilində sıra
    start_time = Column(String, nullable=True)      # "10:00" kimi sərbəst mətn
    notes = Column(Text, nullable=True)

    tour_plan = relationship("TourPlan", back_populates="items")
    place = relationship("Place", back_populates="tour_items")
    restaurant = relationship("Restaurant", back_populates="tour_items")
