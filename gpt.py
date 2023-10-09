import openai
import instructor
from typing import List, Tuple, Dict
import streamlit as st
import enum
from pydantic import BaseModel

instructor.patch()


if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = None


def summarize(document: str) -> str:
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "You're an exceptional lawyer skilled at distilling long contracts into short paragraphs that is easy to understand and digest. Your task is to explain what this contract is, what it does, and what it means to the client.",
            },
            {
                "role": "user",
                "content": f"Provide an executive summary for the following contract: {document}",
            },
        ],
    )

    return res.choices[0].message["content"]


class ContractTypes(str, enum.Enum):
    EMPLOYMENT = "employment"
    LEASE = "lease"
    SALE = "sale"
    SERVICE = "service"
    NON_DISCLOSURE = "non_disclosure"
    OTHER = "other"


class ContractClassification(BaseModel):
    contract_type: ContractTypes


def classify_contract(document: str) -> ContractClassification:
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Determine the type of the following contract: {document}",
            },
        ],
        response_model=ContractClassification,
    )  # type: ignore


def get_obligations(document: str) -> List[str]:
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Highlight the key obligations from the following contract: {document}",
            },
        ],
    )  # type: ignore

    return res.choices[0].message["content"]


def get_party_details(document: str) -> Dict:
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Extract the parties from the following contract: {document}",
            },
        ],
    )  # type: ignore

    return res.choices[0].message["content"]


def extract_important_dates(document: str) -> str:
    """Extract and highlight important dates from the contract."""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": f"There are deadlines in this document and your task is to find them and tell me what I have to do on those dates. You HAVE to find the dates. Here's the document: {document}.",
            },
        ],
    )

    return res.choices[0].message["content"]


def extract_termination_clauses(document: str) -> str:
    """Extract and highlight termination clauses from the contract."""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": f"Highlight the termination clauses in this contract: {document}",
            },
        ],
    )

    return res.choices[0].message["content"]


def highlight_confidentiality_noncompete(document: str) -> str:
    """Highlight confidentiality and non-compete clauses from the contract."""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": f"Identify the confidentiality and non-compete clauses in this contract: {document}",
            },
        ],
    )

    return res.choices[0].message["content"]
