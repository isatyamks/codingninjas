"""
Structured logging utility for the Excel Mock Interviewer.
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("excel_interviewer")
