"""
Mind Map Generation Pipeline (Isolated Module)
-------------------------------------------------
This file contains ONLY the logic used to generate AI-based intelligence mind maps.

Usage:
    from open_notebook.utils.mindmap_engine import MindMapEngine
    engine = MindMapEngine()
    result = engine.generate_mind_map(text)

Dependencies:
    - langchain_core
    - your LLM configuration
"""

import re
import json
import logging
from typing import Dict, Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# -------------------------------------------------
# LOGGER
# -------------------------------------------------
logger = logging.getLogger("MindMapEngine")


class MindMapEngine:
    """Standalone Mind Map Generation Engine"""

    def __init__(self, llm=None):
        logger.info("🧠 Initializing MindMapEngine")
        self.llm = llm

        # ===== LLM PROMPT FOR INTELLIGENCE MIND MAP =====
        self.mindmap_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a professional intelligence analyst building a structured subject intelligence mind map.\n"
                "STRICT RULES:\n"
                "1. Root label MUST be the Subject Name or Document Title.\n"
                "2. Create maximum 6 high-level intelligence categories.\n"
                "3. Categories must be meaningful dimensions such as:\n"
                "   Identity, Background, Criminal History, Legal Status, Gang Affiliations,\n"
                "   Associates, Financial Links, Locations, Modus Operandi, Timeline.\n"
                "4. DO NOT create generic categories like CRIME, MURDER, ATTACK.\n"
                "5. Each child must be a complete factual statement.\n"
                "6. Remove duplicate facts.\n"
                "7. Omit empty categories.\n"
                "8. For each category, create sub-categories if needed for better organization.\n"
                "Return ONLY valid JSON in this format:\n"
                '{ "label": "Subject Name", "children": [ {"label": "Category", "children": [{"label": "Fact"}] } ] }'
            ),
            ("human", "Subject: {person}\nIntelligence Text:\n{context}")
        ])

        if self.llm:
            self.mindmap_chain = self.mindmap_prompt | self.llm | StrOutputParser()

    # -------------------------------------------------
    # ENTITY DETECTION (MAIN PERSON)
    # -------------------------------------------------
    def detect_main_person(self, text: str) -> str:
        """Detect the main person/subject from the text"""
        persons = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", text)
        return max(set(persons), key=persons.count) if persons else "Subject"

    # -------------------------------------------------
    # SAFE JSON PARSER
    # -------------------------------------------------
    def safe_json_load(self, text: str) -> Dict[str, Any]:
        """Safely parse JSON from LLM response"""
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            raise ValueError("Invalid JSON from LLM")

    # -------------------------------------------------
    # REMOVE DUPLICATES & CLEAN TREE
    # -------------------------------------------------
    def deduplicate_mindmap(self, mind_map: Dict) -> Dict:
        """Remove duplicate categories and facts"""
        if not isinstance(mind_map, dict):
            return mind_map

        seen_categories = set()
        clean_children = []

        for category in mind_map.get("children", []):
            label = category.get("label", "").strip()
            if not label or label in seen_categories:
                continue
            seen_categories.add(label)

            seen_facts = set()
            facts = []
            for child in category.get("children", []):
                fact = child.get("label", "").strip()
                if fact and fact not in seen_facts:
                    seen_facts.add(fact)
                    facts.append({"label": fact})

            if facts:
                clean_children.append({"label": label, "children": facts})

        mind_map["children"] = clean_children
        return mind_map

    # -------------------------------------------------
    # FALLBACK RULE-BASED MIND MAP
    # -------------------------------------------------
    def fallback_mindmap(self, person: str, text: str) -> Dict:
        """Generate rule-based mind map when LLM fails"""
        def extract_sentences(pattern, limit=8):
            sentences = re.split(r"(?<=[.!?])\s+", text)
            matches = []
            for s in sentences:
                if re.search(pattern, s, re.I):
                    clean = s.strip()
                    if 20 < len(clean) < 300:
                        matches.append({"label": clean})
                if len(matches) >= limit:
                    break
            return matches

        # Extract incidents
        incident_pattern = r'(\d+(?:ST|ND|RD|TH)?\s*INCIDENT)'
        incident_matches = list(re.finditer(incident_pattern, text, re.IGNORECASE))
        
        children = []
        
        if incident_matches:
            # Criminal case structure
            incidents = []
            for i, match in enumerate(incident_matches[:10]):  # Limit to 10 incidents
                start = match.start()
                end = incident_matches[i+1].start() if i+1 < len(incident_matches) else len(text)
                incident_text = text[start:end].strip()
                incident_title = incident_text.split('\n')[0][:100]
                
                # Extract key facts from incident
                facts = []
                fir_match = re.search(r'FIR\s*NO[.:]?\s*(\d+/\d+)', incident_text, re.IGNORECASE)
                if fir_match:
                    facts.append({"label": f"FIR: {fir_match.group(1)}"})
                
                date_matches = re.findall(r'\b(\d{2}[./]\d{2}[./]\d{4})\b', incident_text)
                if date_matches:
                    facts.append({"label": f"Date: {date_matches[0]}"})
                
                if facts:
                    incidents.append({"label": incident_title, "children": facts})
            
            if incidents:
                children.append({"label": "Criminal Incidents", "children": incidents})
        
        # Add other categories
        children.extend([
            {"label": "Identity & Background", "children": extract_sentences(r"address|village|resident|age|dob|born", 6)},
            {"label": "Family & Associates", "children": extract_sentences(r"father|mother|brother|sister|associate|gang|friend", 6)},
            {"label": "Legal Status", "children": extract_sentences(r"arrest|court|bail|custody|trial|jail|prison", 6)},
        ])
        
        # Remove empty categories
        children = [c for c in children if c.get("children")]

        return {
            "label": person,
            "children": children,
        }

    # -------------------------------------------------
    # MAIN PUBLIC FUNCTION
    # -------------------------------------------------
    def generate_mind_map(self, full_text: str, title: Optional[str] = None) -> Dict:
        """Main API to generate mind map from text"""
        person = title or self.detect_main_person(full_text)

        # If no LLM configured, use fallback
        if not self.llm:
            logger.info("⚠️ No LLM configured, using rule-based fallback")
            return self.fallback_mindmap(person, full_text)

        try:
            logger.info(f"🤖 Generating AI mind map for: {person}")
            raw = self.mindmap_chain.invoke({
                "person": person,
                "context": full_text[:12000]  # Limit context to 12k chars
            })

            mind_map = self.safe_json_load(raw)
            if not mind_map.get("children"):
                raise ValueError("Empty mind map")

            mind_map = self.deduplicate_mindmap(mind_map)
            logger.info("✅ LLM Mind Map Generated")
            return mind_map

        except Exception as e:
            logger.warning(f"⚠️ LLM mind map failed, using fallback: {e}")
            return self.fallback_mindmap(person, full_text)
