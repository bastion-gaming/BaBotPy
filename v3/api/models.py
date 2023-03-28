from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Date, DateTime, Float, Interval, Text, Time, Unicode, UnicodeText
from sqlalchemy.orm import relationship
import datetime as dt

from .database import Base


class TableCore(Base):

    __tablename__ = "core"

    playerid = Column(BigInteger, primary_key=True, index=True)
    discord_id = Column(String)
    arrival = Column(String)
    level = Column(Integer)
    xp = Column(BigInteger)
    devise = Column(BigInteger)
    super_devise = Column(BigInteger)
    godparent = Column(BigInteger)
    nbreaction = Column(BigInteger)
    nbmsg = Column(BigInteger)

    core_old = relationship("TableCoreOld", back_populates="owner")
    com_time = relationship("TableComTime", back_populates="owner")


class TableCoreOld(Base):

    __tablename__ = "core_old"

    playerid = Column(BigInteger, ForeignKey("core.playerid"), primary_key=True)
    discord_id = Column(String)
    level = Column(Integer)
    xp = Column(BigInteger)

    owner = relationship("TableCore", back_populates="core_old")


class TableComTime(Base):

    __tablename__ = "com_time"

    playerid = Column(BigInteger, ForeignKey("core.playerid"), primary_key=True)
    command = Column(String, primary_key=True)
    time = Column(String)

    owner = relationship("TableCore", back_populates="com_time")


# class Table(Base):
#
#     __tablename__=""
#
#     playerid = Column(BigInteger, ForeignKey("core.playerid"), primary_key=True)
#
#     owner = relationship("TableCore", back_populates="")
