from enum import Enum


class OrganizationStatus(Enum):
    DRAFT = "DRAFT"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    APPROVED = "APPROVED"
    PUBLISH_IN_PROGRESS = "PUBLISH_IN_PROGRESS"
    PUBLISHED = "PUBLISHED"


class PostOrganizationActions(Enum):
    DRAFT = "draft"
    SUBMIT = "submit"


class MemberRole(Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"