#!/usr/bin/env python3
"""
Intent Classifier for Personal Coaching Assistant
Classifies incoming messages into categories for appropriate response routing.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

class MessageIntent(Enum):
    """Possible intents for incoming messages."""
    EMOTIONAL = "emotional"          # Feelings, emotions, stress, overwhelm
    PRACTICAL = "practical"          # Task-oriented, planning, logistics
    REFLECTIVE = "reflective"        # Self-awareness, values, meaning
    MOTIVATIONAL = "motivational"    # Need encouragement, stuck, procrastinating
    SOCIAL = "social"               # Relationships, communication issues
    DECISION = "decision"           # Need help choosing, weighing options
    PROGRESS = "progress"           # Updates on goals, achievements, setbacks
    GENERAL = "general"             # Casual conversation, unclear intent

@dataclass
class IntentResult:
    """Result of intent classification."""
    intent: MessageIntent
    confidence: float
    keywords: List[str]
    reasoning: str

class IntentClassifier:
    """
    Classifies message intent using keyword matching and pattern recognition.
    
    This is a rule-based approach that can be enhanced with ML models later.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Intent keywords and patterns
        self.intent_patterns = {
            MessageIntent.EMOTIONAL: {
                "keywords": [
                    "feel", "feeling", "emotions", "stressed", "anxious", "overwhelmed",
                    "frustrated", "angry", "sad", "depressed", "worried", "scared",
                    "excited", "happy", "grateful", "confused", "lost", "empty",
                    "tired", "exhausted", "drained", "burnout", "pressure"
                ],
                "phrases": [
                    "i feel", "i'm feeling", "feeling like", "i'm so", "makes me feel",
                    "i'm stressed", "i'm anxious", "i'm overwhelmed", "emotional about",
                    "can't handle", "breaking down", "falling apart"
                ],
                "patterns": [
                    r"i feel\s+\w+",
                    r"i'm\s+(so\s+)?(stressed|anxious|overwhelmed|tired|frustrated)",
                    r"feeling\s+(really\s+)?\w+",
                    r"makes me\s+(feel\s+)?\w+"
                ]
            },
            
            MessageIntent.PRACTICAL: {
                "keywords": [
                    "plan", "planning", "schedule", "organize", "task", "todo", "list",
                    "project", "work", "deadline", "meeting", "calendar", "time",
                    "budget", "money", "logistics", "system", "process", "method",
                    "strategy", "approach", "steps", "how to", "what should"
                ],
                "phrases": [
                    "how do i", "what should i do", "need to plan", "help me organize",
                    "what's the best way", "how can i", "need to get", "have to do",
                    "deadline is", "meeting tomorrow", "project is due"
                ],
                "patterns": [
                    r"how\s+(do\s+i|can\s+i)\s+\w+",
                    r"what\s+(should|can)\s+i\s+\w+",
                    r"need\s+to\s+(plan|organize|schedule)",
                    r"help\s+me\s+(plan|organize|figure out)",
                    r"what's\s+the\s+best\s+way"
                ]
            },
            
            MessageIntent.REFLECTIVE: {
                "keywords": [
                    "meaning", "purpose", "values", "beliefs", "identity", "who am i",
                    "why do i", "what's the point", "reflection", "think about",
                    "philosophy", "principles", "life", "existence", "spiritual",
                    "growth", "learning", "wisdom", "insight", "understanding"
                ],
                "phrases": [
                    "what's the meaning", "what's the point", "who am i", "why do i",
                    "what do i believe", "what matters", "life purpose", "my values",
                    "thinking about", "wondering about", "reflecting on", "makes me think"
                ],
                "patterns": [
                    r"what's\s+the\s+(meaning|point|purpose)",
                    r"who\s+am\s+i",
                    r"why\s+do\s+i\s+\w+",
                    r"what\s+do\s+i\s+(believe|value|think)",
                    r"(thinking|wondering|reflecting)\s+(about|on)"
                ]
            },
            
            MessageIntent.MOTIVATIONAL: {
                "keywords": [
                    "stuck", "procrastinating", "motivation", "unmotivated", "lazy",
                    "can't start", "giving up", "quit", "discouraged", "hopeless",
                    "failed", "failure", "trying", "struggling", "difficult",
                    "impossible", "can't do", "too hard", "overwhelming"
                ],
                "phrases": [
                    "i'm stuck", "can't get started", "keep procrastinating", "want to give up",
                    "lost motivation", "don't feel like", "too difficult", "can't do this",
                    "feeling discouraged", "not making progress", "keep failing"
                ],
                "patterns": [
                    r"i'm\s+(stuck|procrastinating|unmotivated)",
                    r"can't\s+(get\s+started|start|do)",
                    r"keep\s+(procrastinating|failing|trying)",
                    r"want\s+to\s+(give\s+up|quit)",
                    r"(lost|losing)\s+motivation"
                ]
            },
            
            MessageIntent.SOCIAL: {
                "keywords": [
                    "relationship", "friends", "family", "colleague", "boss", "partner",
                    "conflict", "argument", "communication", "social", "people",
                    "conversation", "awkward", "difficult person", "boundaries"
                ],
                "phrases": [
                    "had an argument", "conflict with", "relationship issue", "friend said",
                    "family drama", "work politics", "difficult conversation", "social anxiety",
                    "don't know how to talk", "relationship problem"
                ],
                "patterns": [
                    r"(relationship|conflict|argument)\s+with",
                    r"(friend|family|colleague|boss|partner)\s+(said|did|is)",
                    r"difficult\s+(person|conversation)",
                    r"don't\s+know\s+how\s+to\s+(talk|communicate|handle)"
                ]
            },
            
            MessageIntent.DECISION: {
                "keywords": [
                    "decision", "choose", "choice", "option", "should i", "or",
                    "versus", "vs", "pros and cons", "decide", "unsure", "torn between",
                    "dilemma", "advice", "what would you do", "recommend"
                ],
                "phrases": [
                    "should i", "which should i", "can't decide", "torn between", "unsure about",
                    "what would you do", "what do you think", "need advice", "help me choose",
                    "pros and cons", "decision between"
                ],
                "patterns": [
                    r"should\s+i\s+\w+",
                    r"(can't|cannot)\s+decide",
                    r"torn\s+between",
                    r"(unsure|uncertain)\s+(about|whether)",
                    r"what\s+(would\s+you\s+do|do\s+you\s+think)",
                    r"\w+\s+or\s+\w+"
                ]
            },
            
            MessageIntent.PROGRESS: {
                "keywords": [
                    "update", "progress", "accomplished", "achieved", "completed", "done",
                    "finished", "success", "failed", "setback", "milestone", "goal",
                    "target", "result", "outcome", "improvement", "better", "worse"
                ],
                "phrases": [
                    "i did", "i completed", "i finished", "i achieved", "made progress",
                    "had a setback", "didn't achieve", "fell short", "reached my goal",
                    "update on", "progress report", "how did", "result was"
                ],
                "patterns": [
                    r"i\s+(did|completed|finished|achieved|accomplished)",
                    r"(made|had|reached)\s+(progress|setback|goal)",
                    r"(didn't|failed\s+to)\s+(achieve|complete|reach)",
                    r"(update|progress)\s+on"
                ]
            }
        }
    
    def classify_intent(self, message: str) -> IntentResult:
        """
        Classify the intent of an incoming message.
        
        Args:
            message: The message text to classify
            
        Returns:
            IntentResult with intent, confidence, and reasoning
        """
        message_lower = message.lower().strip()
        
        # Calculate scores for each intent
        intent_scores = {}
        matched_keywords = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            keywords = []
            
            # Check keywords
            for keyword in patterns["keywords"]:
                if keyword in message_lower:
                    score += 1
                    keywords.append(keyword)
            
            # Check phrases (weighted higher)
            for phrase in patterns["phrases"]:
                if phrase in message_lower:
                    score += 2
                    keywords.append(phrase)
            
            # Check regex patterns (weighted highest)
            for pattern in patterns["patterns"]:
                if re.search(pattern, message_lower):
                    score += 3
                    keywords.append(f"pattern: {pattern}")
            
            intent_scores[intent] = score
            matched_keywords[intent] = keywords
        
        # Find the intent with highest score
        if not any(intent_scores.values()):
            # No patterns matched - default to general
            return IntentResult(
                intent=MessageIntent.GENERAL,
                confidence=0.5,
                keywords=[],
                reasoning="No specific patterns matched - general conversation"
            )
        
        best_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[best_intent]
        
        # Calculate confidence (normalize by message length and max possible score)
        confidence = min(max_score / max(len(message_lower.split()) * 0.3, 3), 1.0)
        
        # Generate reasoning
        reasoning = f"Matched {max_score} patterns for {best_intent.value}"
        if matched_keywords[best_intent]:
            reasoning += f" (keywords: {', '.join(matched_keywords[best_intent][:3])})"
        
        return IntentResult(
            intent=best_intent,
            confidence=confidence,
            keywords=matched_keywords[best_intent],
            reasoning=reasoning
        )
    
    def get_response_strategy(self, intent: MessageIntent) -> Dict[str, str]:
        """
        Get response strategy based on intent.
        
        Args:
            intent: The classified intent
            
        Returns:
            Dictionary with response guidelines
        """
        strategies = {
            MessageIntent.EMOTIONAL: {
                "tone": "empathetic and validating",
                "approach": "acknowledge feelings, provide emotional support, suggest coping strategies",
                "example_starters": ["I hear that you're feeling...", "It sounds like...", "That must be..."]
            },
            
            MessageIntent.PRACTICAL: {
                "tone": "helpful and solution-oriented",
                "approach": "provide concrete steps, break down tasks, offer organizational methods",
                "example_starters": ["Let's break this down...", "Here's what I suggest...", "You could try..."]
            },
            
            MessageIntent.REFLECTIVE: {
                "tone": "thoughtful and inquiry-based",
                "approach": "ask probing questions, connect to values, encourage deeper thinking",
                "example_starters": ["What does this mean to you?", "How does this align with...", "Consider..."]
            },
            
            MessageIntent.MOTIVATIONAL: {
                "tone": "encouraging and action-oriented",
                "approach": "provide motivation, suggest small first steps, reframe challenges",
                "example_starters": ["You can do this...", "Let's start small...", "Remember that..."]
            },
            
            MessageIntent.SOCIAL: {
                "tone": "understanding and diplomatic",
                "approach": "explore perspectives, suggest communication strategies, validate concerns",
                "example_starters": ["Relationships can be complex...", "Have you considered...", "It might help to..."]
            },
            
            MessageIntent.DECISION: {
                "tone": "balanced and analytical",
                "approach": "help weigh options, clarify values, suggest decision frameworks",
                "example_starters": ["Let's think through...", "What matters most to you?", "Consider the pros and cons..."]
            },
            
            MessageIntent.PROGRESS: {
                "tone": "encouraging and reflective",
                "approach": "celebrate wins, learn from setbacks, plan next steps",
                "example_starters": ["That's great progress...", "What did you learn from...", "Next, you could..."]
            },
            
            MessageIntent.GENERAL: {
                "tone": "friendly and open",
                "approach": "engage naturally, ask clarifying questions, maintain conversation",
                "example_starters": ["Tell me more about...", "I'm here to help...", "What's on your mind?"]
            }
        }
        
        return strategies.get(intent, strategies[MessageIntent.GENERAL])

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    classifier = IntentClassifier()
    
    # Test messages
    test_messages = [
        "I feel so overwhelmed with everything going on",
        "How should I organize my schedule for next week?",
        "What's the meaning of all this work I'm doing?",
        "I'm stuck and can't get started on this project",
        "Had an argument with my friend yesterday",
        "Should I take this job offer or stay at my current position?",
        "I completed my goal of running 5k today!",
        "Hey, how are you doing?"
    ]
    
    print("🧠 Intent Classification Test Results")
    print("=" * 50)
    
    for message in test_messages:
        result = classifier.classify_intent(message)
        strategy = classifier.get_response_strategy(result.intent)
        
        print(f"\n📨 Message: '{message}'")
        print(f"🎯 Intent: {result.intent.value} (confidence: {result.confidence:.2f})")
        print(f"💭 Reasoning: {result.reasoning}")
        print(f"📋 Strategy: {strategy['approach']}")
        print(f"🗣️  Tone: {strategy['tone']}") 