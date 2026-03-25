from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

@dataclass
class Member:
    address: str
    join_date: datetime
    reputation_score: float
    voting_history: List[str]

class GovernanceRules:
    def __init__(self):
        self.members: Dict[str, Member] = {}
        self.min_reputation_for_proposal = 100
        self.base_voting_weight = 1.0
        self.max_voting_weight = 10.0
        
    def calculate_voting_weight(self, member_address: str) -> float:
        """Calculate a member's voting weight based on reputation and tenure"""
        member = self.members.get(member_address)
        if not member:
            return 0.0
            
        # Base components for weight calculation
        tenure_weight = self._calculate_tenure_weight(member.join_date)
        reputation_weight = self._calculate_reputation_weight(member.reputation_score)
        participation_weight = self._calculate_participation_weight(member.voting_history)
        
        # Combine weights with dampening
        total_weight = (
            self.base_voting_weight *
            (tenure_weight * 0.3 +
             reputation_weight * 0.5 +
             participation_weight * 0.2)
        )
        
        return min(total_weight, self.max_voting_weight)
    
    def _calculate_tenure_weight(self, join_date: datetime) -> float:
        """Calculate weight modifier based on member tenure"""
        days_active = (datetime.now() - join_date).days
        return min(days_active / 365, 1.0)  # Max tenure weight after 1 year
    
    def _calculate_reputation_weight(self, reputation: float) -> float:
        """Calculate weight modifier based on reputation score"""
        return min(reputation / 1000, 1.0)  # Normalize to max 1.0
    
    def _calculate_participation_weight(self, voting_history: List[str]) -> float:
        """Calculate weight modifier based on governance participation"""
        if not voting_history:
            return 0.0
        
        recent_votes = len([vote for vote in voting_history 
                          if self._is_recent(vote)])
        return min(recent_votes / 10, 1.0)  # Max weight after 10 recent votes
    
    def _is_recent(self, vote_id: str) -> bool:
        """Check if a vote occurred within the last 30 days"""
        try:
            vote_date = datetime.fromisoformat(vote_id.split('-')[0])
            return (datetime.now() - vote_date) <= timedelta(days=30)
        except:
            return False
    
    def can_create_proposal(self, member_address: str) -> bool:
        """Check if a member has sufficient reputation to create proposals"""
        member = self.members.get(member_address)
        return member and member.reputation_score >= self.min_reputation_for_proposal
    
    def register_member(self, address: str) -> None:
        """Register a new member with initial values"""
        if address not in self.members:
            self.members[address] = Member(
                address=address,
                join_date=datetime.now(),
                reputation_score=0.0,
                voting_history=[]
            )
    
    def record_vote(self, member_address: str, proposal_id: str) -> None:
        """Record a member's vote participation"""
        if member_address in self.members:
            vote_id = f"{datetime.now().isoformat()}-{proposal_id}"
            self.members[member_address].voting_history.append(vote_id)
