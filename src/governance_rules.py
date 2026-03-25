from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime

class VotingThreshold:
    def __init__(self, min_quorum: Decimal, scaling_factor: Decimal = Decimal('0.5')):
        self.min_quorum = min_quorum
        self.scaling_factor = scaling_factor

    def calculate_required_quorum(self, total_stake: Decimal, proposal_impact: Decimal) -> Decimal:
        """Calculate required quorum based on proposal impact and total stake"""
        return min(
            self.min_quorum + (proposal_impact * self.scaling_factor),
            Decimal('1.0')
        )

class GovernanceRules:
    def __init__(self):
        self.voting_thresholds = VotingThreshold(min_quorum=Decimal('0.2'))
        self.proposal_categories = {
            'CRITICAL': Decimal('0.8'),
            'HIGH': Decimal('0.6'),
            'MEDIUM': Decimal('0.4'),
            'LOW': Decimal('0.2')
        }
        self.voting_period_days = 7

    def validate_proposal(self, proposal: Dict) -> bool:
        """Validate if a proposal meets basic governance rules"""
        required_fields = ['title', 'description', 'category', 'start_time']
        return all(field in proposal for field in required_fields)

    def calculate_vote_result(self,
                            votes: List[Dict],
                            total_stake: Decimal,
                            proposal_category: str) -> Dict:
        """Calculate voting results with dynamic thresholds"""
        if not votes:
            return {'passed': False, 'reason': 'No votes cast'}

        positive_votes = sum(Decimal(v['stake']) for v in votes if v['vote'] == 'YES')
        total_votes = sum(Decimal(v['stake']) for v in votes)

        impact_level = self.proposal_categories.get(proposal_category, Decimal('0.4'))
        required_quorum = self.voting_thresholds.calculate_required_quorum(
            total_stake,
            impact_level
        )

        participation_rate = total_votes / total_stake
        approval_rate = positive_votes / total_votes if total_votes > 0 else Decimal('0')

        result = {
            'passed': False,
            'participation_rate': float(participation_rate),
            'approval_rate': float(approval_rate),
            'required_quorum': float(required_quorum)
        }

        if participation_rate >= required_quorum and approval_rate >= Decimal('0.5'):
            result['passed'] = True

        return result

    def is_voting_active(self, proposal_start_time: datetime) -> bool:
        """Check if voting period is still active"""
        elapsed_days = (datetime.now() - proposal_start_time).days
        return elapsed_days <= self.voting_period_days

    def get_proposal_requirements(self, category: str) -> Dict:
        """Get specific requirements for a proposal category"""
        return {
            'impact_level': float(self.proposal_categories.get(category, Decimal('0.4'))),
            'voting_period_days': self.voting_period_days,
            'min_quorum': float(self.voting_thresholds.min_quorum)
        }
