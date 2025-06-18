from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    inn = Column(String(12), unique=True, nullable=False, index=True)  # ИНН - 10 или 12 цифр
    identifier = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с банковскими счетами
    accounts = relationship("BankAccount", back_populates="company", cascade="all, delete-orphan")

class Bank(Base):
    __tablename__ = "banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    identifier = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с банковскими счетами
    accounts = relationship("BankAccount", back_populates="bank", cascade="all, delete-orphan")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), nullable=False, index=True)
    identifier = Column(String(50), unique=True, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи с компанией и банком
    company = relationship("Company", back_populates="accounts")
    bank = relationship("Bank", back_populates="accounts")
    
    # Уникальное ограничение: номер счета должен быть уникален в пределах одного банка
    __table_args__ = (
        UniqueConstraint('account_number', 'bank_id', name='_account_bank_uc'),
    ) 