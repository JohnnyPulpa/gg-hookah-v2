"""
GG HOOKAH v2 — SQLAlchemy models
Section 7 of GG_HOOKAH_Spec_Master_v2_1.docx
"""
from sqlalchemy import (
    Column, Text, Integer, SmallInteger, Boolean,
    DateTime, ForeignKey, Index, UniqueConstraint, CheckConstraint,
    text as sa_text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, BIGINT
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    telegram_id = Column(BIGINT, unique=True, nullable=False)
    username = Column(Text, nullable=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    language = Column(Text, nullable=False, server_default="ru")
    theme = Column(Text, nullable=False, server_default="light")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Guest(Base):
    __tablename__ = "guests"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    phone = Column(Text, unique=True, nullable=False)
    telegram_id = Column(BIGINT, nullable=True, index=True)
    name = Column(Text, nullable=True)
    passport_photo_url = Column(Text, nullable=True)
    passport_uploaded_at = Column(DateTime(timezone=True), nullable=True)
    trust_flag = Column(Text, nullable=False, server_default="normal")
    notes = Column(Text, nullable=True)
    total_orders = Column(Integer, nullable=False, server_default="0")
    total_rebowls = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_guests_trust_flag", "trust_flag"),
    )


class Mix(Base):
    __tablename__ = "mixes"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    name = Column(Text, nullable=False)
    flavors = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    strength = Column(SmallInteger, nullable=False, server_default="3")
    coolness = Column(SmallInteger, nullable=False, server_default="3")
    sweetness = Column(SmallInteger, nullable=False, server_default="3")
    smokiness = Column(SmallInteger, nullable=False, server_default="3")
    details = Column(Text, nullable=True)
    image_url = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    sort_order = Column(Integer, nullable=False, server_default="0")
    is_featured = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint("strength BETWEEN 1 AND 5", name="ck_mixes_strength"),
        CheckConstraint("coolness BETWEEN 1 AND 5", name="ck_mixes_coolness"),
        CheckConstraint("sweetness BETWEEN 1 AND 5", name="ck_mixes_sweetness"),
        CheckConstraint("smokiness BETWEEN 1 AND 5", name="ck_mixes_smokiness"),
        Index("ix_mixes_active_sort", "is_active", "sort_order"),
    )


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    item_type = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    price_gel = Column(Integer, nullable=False)
    image_url = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="true")
    sort_order = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_menu_items_type_active_sort", "item_type", "is_active", "sort_order"),
    )


class Discount(Base):
    __tablename__ = "discounts"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    phone = Column(Text, nullable=False)
    percent = Column(SmallInteger, nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, nullable=False, server_default="false")
    used_at = Column(DateTime(timezone=True), nullable=True)
    used_order_id = Column(UUID(as_uuid=True), nullable=True)
    issued_by_admin_telegram_id = Column(BIGINT, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_discounts_phone", "phone"),
        Index("ix_discounts_valid_until", "valid_until"),
        Index("ix_discounts_is_used", "is_used"),
        Index(
            "uq_discounts_one_active_per_phone", "phone",
            unique=True,
            postgresql_where=sa_text("is_used = false"),
        ),
    )


class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"), nullable=True)
    telegram_id = Column(BIGINT, nullable=False)
    phone = Column(Text, nullable=False)
    hookah_count = Column(SmallInteger, nullable=False, server_default="1")
    status = Column(Text, nullable=False, server_default="NEW")
    mix_id = Column(UUID(as_uuid=True), ForeignKey("mixes.id"), nullable=False)
    address_text = Column(Text, nullable=False)
    entrance = Column(Text, nullable=True)
    floor = Column(Text, nullable=True)
    apartment = Column(Text, nullable=True)
    door_code = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    requested_time = Column(DateTime(timezone=True), nullable=True)
    promised_time = Column(DateTime(timezone=True), nullable=True)
    promised_eta_text = Column(Text, nullable=True)
    deposit_type = Column(Text, nullable=False, server_default="cash")
    deposit_amount_gel = Column(Integer, nullable=False, server_default="100")
    discount_id = Column(UUID(as_uuid=True), ForeignKey("discounts.id"), nullable=True)
    promo_code = Column(Text, nullable=True)
    promo_percent = Column(SmallInteger, nullable=True)
    discount_percent = Column(SmallInteger, nullable=True)
    is_late_order = Column(Boolean, nullable=False, server_default="false")
    admin_note = Column(Text, nullable=True)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    departed_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    session_started_at = Column(DateTime(timezone=True), nullable=True)
    session_ends_at = Column(DateTime(timezone=True), nullable=True)
    free_extension_used = Column(Boolean, nullable=False, server_default="false")
    pickup_requested_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    cancel_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint("hookah_count BETWEEN 1 AND 3", name="ck_orders_hookah_count"),
        Index("ix_orders_status", "status"),
        Index("ix_orders_telegram_id", "telegram_id"),
        Index("ix_orders_phone", "phone"),
        Index("ix_orders_created_at", "created_at"),
        Index("ix_orders_session_ends_at", "session_ends_at"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(Text, nullable=False)
    mix_id = Column(UUID(as_uuid=True), ForeignKey("mixes.id"), nullable=True)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"), nullable=True)
    quantity = Column(Integer, nullable=False, server_default="1")
    unit_price_gel = Column(Integer, nullable=False)
    total_price_gel = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        Index("ix_order_items_item_type", "item_type"),
    )


class RebowlRequest(Base):
    __tablename__ = "rebowl_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    requested_by_telegram_id = Column(BIGINT, nullable=False)
    mix_id = Column(UUID(as_uuid=True), ForeignKey("mixes.id"), nullable=False)
    price_gel = Column(Integer, nullable=False, server_default="50")
    add_minutes = Column(Integer, nullable=False, server_default="120")
    status = Column(Text, nullable=False, server_default="REQUESTED")
    requested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    in_progress_at = Column(DateTime(timezone=True), nullable=True)
    done_at = Column(DateTime(timezone=True), nullable=True)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    admin_note = Column(Text, nullable=True)
    __table_args__ = (
        Index("ix_rebowl_requests_order_id", "order_id"),
        Index("ix_rebowl_requests_status", "status"),
        Index(
            "uq_rebowl_one_active_per_order", "order_id",
            unique=True,
            postgresql_where=sa_text("status IN ('REQUESTED', 'IN_PROGRESS')"),
        ),
    )


class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    code = Column(Text, unique=True, nullable=False)
    percent = Column(SmallInteger, nullable=False)
    max_uses = Column(Integer, nullable=False, server_default="10")
    used_count = Column(Integer, nullable=False, server_default="0")
    valid_from = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    valid_until = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_by_admin_telegram_id = Column(BIGINT, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_promo_codes_is_active", "is_active"),
        Index("ix_promo_codes_valid_until", "valid_until"),
    )


class PromoCodeUsage(Base):
    __tablename__ = "promo_code_usages"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    promo_code_id = Column(UUID(as_uuid=True), ForeignKey("promo_codes.id", ondelete="CASCADE"), nullable=False)
    phone = Column(Text, nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint("promo_code_id", "phone", name="uq_promo_usage_per_phone"),
    )


class SupportMessage(Base):
    __tablename__ = "support_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    thread_type = Column(Text, nullable=False)
    thread_id = Column(UUID(as_uuid=True), nullable=True)
    telegram_user_id = Column(BIGINT, nullable=False)
    direction = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_read = Column(Boolean, nullable=False, server_default="false")
    __table_args__ = (
        Index("ix_support_messages_thread", "thread_type", "thread_id"),
        Index("ix_support_messages_telegram_user_id", "telegram_user_id"),
        Index("ix_support_messages_is_read", "is_read"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sa_text("gen_random_uuid()"))
    entity_type = Column(Text, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(Text, nullable=False)
    details = Column(JSONB, nullable=True)
    admin_telegram_id = Column(BIGINT, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_audit_logs_entity", "entity_type", "entity_id"),
        Index("ix_audit_logs_admin", "admin_telegram_id"),
        Index("ix_audit_logs_created_at", "created_at"),
    )


class Setting(Base):
    __tablename__ = "settings"
    key = Column(Text, primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_by_admin_telegram_id = Column(BIGINT, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
