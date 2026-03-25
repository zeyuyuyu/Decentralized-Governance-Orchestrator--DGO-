from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import math

class VotingStrategy(Enum):
    SIMPLE_MAJORITY = 'simple_majority'
    SUPER_MAJORITY = 'super_majority' 
    UNANIMOUS = 'unanimous'
    QUADRATIC = 'quadratic'

@dataclass
class Role:
    name: str
    voting_power: float
    min_tokens_required: int

@dataclass 
class Proposal:
    id: str
    title: str
    description: str
    creator: str
    required_strategy: VotingStrategy
    min_participation: float
    votes_for: Dict[str, float] = None
    votes_against: Dict[str, float] = None
    
    def __post_init__(self):
        self.votes_for = {}
        self.votes_against = {}

class GovernanceRules:
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.proposals: Dict[str, Proposal] = {}
        
    def add_role(self, name: str, voting_power: float, min_tokens: int) -> None:
        """Add a new governance role with specified voting power"""
        self.roles[name] = Role(name, voting_power, min_tokens)
    
    def create_proposal(self, id: str, title: str, description: str,
                       creator: str, strategy: VotingStrategy,
                       min_participation: float) -> Proposal:
        """Create a new governance proposal"""
        proposal = Proposal(id, title, description, creator,
                          strategy, min_participation)
        self.proposals[id] = proposal
        return proposal

    def cast_vote(self, proposal_id: str, voter: str,
                  role: str, vote_for: bool,
                  token_weight: float) -> bool:
        """Cast a weighted vote on a proposal"""
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        if role not in self.roles:
            raise ValueError('Invalid role')
            
        proposal = self.proposals[proposal_id]
        vote_power = token_weight * self.roles[role].voting_power
        
        if vote_for:
            proposal.votes_for[voter] = vote_power
        else:
            proposal.votes_against[voter] = vote_power
            
        return True

    def get_vote_result(self, proposal_id: str) -> Optional[bool]:
        """Calculate the result of a proposal vote"""
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        proposal = self.proposals[proposal_id]
        total_for = sum(proposal.votes_for.values())
        total_against = sum(proposal.votes_against.values())
        total_votes = total_for + total_against
        
        if total_votes == 0:
            return None
            
        # Check minimum participation
        if total_votes < proposal.min_participation:
            return None
            
        if proposal.required_strategy == VotingStrategy.SIMPLE_MAJORITY:
            return total_for > total_against
            
        elif proposal.required_strategy == VotingStrategy.SUPER_MAJORITY:
            return total_for >= (2/3 * total_votes)
            
        elif proposal.required_strategy == VotingStrategy.UNANIMOUS:
            return total_against == 0 and total_for > 0
            
        elif proposal.required_strategy == VotingStrategy.QUADRATIC:
            # Square root of token weights for quadratic voting
            sqrt_for = sum(math.sqrt(v) for v in proposal.votes_for.values())
            sqrt_against = sum(math.sqrt(v) for v in proposal.votes_against.values())
            return sqrt_for > sqrt_against
            
        return None