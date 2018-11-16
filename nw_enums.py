
import enum


class Flags(enum.Enum):
    brief = 'brief'
    detailed = 'detailed'
class Events(enum.Enum):
    declared_defender = 'declared_defender'
    performing_attack = 'performing_attack'
    engagement_phase_start = 'engagement_phase_start'