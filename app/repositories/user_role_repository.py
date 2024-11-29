from operator import and_
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.model_user import Role, UserRole


class UserRoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_roles_by_user_id(self, user_id: int):
        return (
            self.session.query(Role)
            .join(
                UserRole,
                and_(UserRole.role_id == Role.id, UserRole.is_deleted == False),
            )
            .filter(UserRole.user_id == user_id)
            .all()
        )

    def get_role_names_by_user_id(self, user_id: int):
        roles = (
            self.session.query(Role.name)
            .join(
                UserRole,
                and_(UserRole.role_id == Role.id, Role.is_deleted == False),
            )
            .filter(and_(UserRole.user_id == user_id, UserRole.is_deleted == False))
            .all()
        )
        return [role.name for role in roles]

    def assign_role_to_user(self, user_id: int, role_id: int):
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.session.add(user_role)
        self.session.commit()

    def remove_role_from_user(self, user_id: int, role_id: int):
        user_role = (
            self.session.query(UserRole)
            .filter_by(user_id=user_id, role_id=role_id)
            .first()
        )
        if user_role:
            user_role.is_deleted = True
            self.session.commit()


def get_user_role_repository(session: Session = Depends(get_db)):
    return UserRoleRepository(session)

    # def get_roles_by_user_id(self, user_id: int):
    #     # Aliased bảng Role
    #     RoleAlias = aliased(Role)

    #     # Truy vấn ORM
    #     query = (
    #         self.session.query(
    #             User.id.label("user_id"),
    #             User.full_name,
    #             User.user_name,
    #             User.email,
    #             User.phone,
    #             User.gender,
    #             User.date_of_birth,
    #             User.status,
    #             User.level,
    #             RoleAlias.id.label("role_id"),
    #             RoleAlias.name.label("role_name"),
    #             RoleAlias.description.label("role_description"),
    #         )
    #         .join(user_roles, user_roles.c.user_id == User.id)
    #         .join(RoleAlias, RoleAlias.id == user_roles.c.role_id)
    #         .filter(User.id == user_id)
    #     )
    #     return query.all()

    # def get_roles_by_user_id(self, user_id: int):
    #     # return self.session.query(user_roles).filter(user_roles.c.user_id == user_id).all()
    #     # return(
    #     #     self.session.query(Role)
    #     #     .join(user_roles, user_roles.c.role_id == Role.id)
    #     #     .filter(user_roles.c.user_id == user_id)
    #     #     # .all()
    #     # )
    #         # Truy vấn thông tin user và roles bằng raw SQL
    #     query = text("""
    #         SELECT
    #             u.id AS user_id,
    #             u.full_name,
    #             u.user_name,
    #             u.email,
    #             u.phone,
    #             u.gender,
    #             u.date_of_birth,
    #             u.status,
    #             u.level,
    #             r.id AS role_id,
    #             r.name AS role_name,
    #             r.description AS role_description
    #         FROM public."user" u
    #         LEFT JOIN user_roles ur ON ur.user_id = u.id
    #         LEFT JOIN role r ON r.id = ur.role_id
    #         WHERE u.id = :user_id
    #     """)
    #     return self.session.execute(query, {"user_id": user_id}).fetchall()
