from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 数据库实例
db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)  # 0: 超级管理员, 1: 租户管理员, 2: 评估师, 3: 审核员

# 项目表
class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    requirement = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('Tenant.id'), nullable=False)  # 外键改为 Tenant.id

    # 设置与 Tenant 表的关系
    owner = db.relationship('Tenant', back_populates='projects')

class Tenant(db.Model):
    __tablename__ = 'Tenant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # 设置与 Project 表的关系
    projects = db.relationship('Project', back_populates='owner', cascade='all, delete-orphan')

# # 项目与分析师关系表
# class ProjectEstimator(db.Model):
#     __tablename__ = 'ProjectEstimator'
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
#     estimator_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class ProjectUserLink(db.Model):
    __tablename__ = 'ProjectUserLink'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


# 功能点表
class FunctionPoint(db.Model):
    __tablename__ = 'FunctionPoint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    project_id = db.Column(db.Integer, nullable=False)  # 对应项目ID
    name = db.Column(db.String(100), nullable=False)  # 功能点名称
    type = db.Column(db.Enum('ILF', 'EIF', 'EI', 'EO', 'EQ'), nullable=False)  # 功能点类型
    complexity = db.Column(db.Enum('LOW', 'MEDIUM', 'HIGH'), nullable=False)  # 复杂度
    base_value = db.Column(db.Integer, nullable=False)  # 基础值
    comment = db.Column(db.Text, nullable=True)  # 功能点备注
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间

class CalculationResult(db.Model):
    __tablename__ = 'CalculationResult'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    project_id = db.Column(db.Integer, nullable=False)  # 项目ID
    GSC_AFP = db.Column(db.Float, nullable=False)  # 调整后的功能点，原AFP
    UFP = db.Column(db.Float, nullable=False)  # 未调整的功能点
    SCF_AFP = db.Column(db.Float, nullable=False)  # 简单复杂度因子，原SCF
    VAF = db.Column(db.Float, nullable=False)  # 系统通用特性，原GSC
    total_weight = db.Column(db.Float, nullable=False)  # VAF总权重
    scf_stage = db.Column(db.Integer, nullable=False)  # SCF阶段
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
