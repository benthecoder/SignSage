import streamlit as st
import openai
from dropbox import DropboxSignClient
from docparser import get_text
import base64
from gpt import (
    summarize,
    classify_contract,
    get_obligations,
    get_party_details,
    extract_important_dates,
    extract_termination_clauses,
    highlight_confidentiality_noncompete,
)

st.set_page_config(
    page_title="SignSage 🔮📜",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dropbox_api_key" not in st.session_state:
    st.session_state["dropbox_api_key"] = None


def sidebar():
    st.sidebar.header("API Key")
    api_key = st.sidebar.text_input("Enter your API key here:")
    st.sidebar.write(
        "Get your API key from [Dropbox](https://www.dropbox.com/developers/apps)"
    )
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key here:")
    st.sidebar.write(
        "Get your API key from [OpenAI](https://platform.openai.com/account/api-keys)"
    )

    if st.sidebar.button("Submit"):
        st.session_state["dropbox_api_key"] = api_key
        st.session_state["openai_api_key"] = openai_api_key


def displayPDF(upl_file, ui_width):
    base64_pdf = base64.b64encode(upl_file).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_data(show_spinner="Extracting important dates ...")
def important_dates(text):
    with st.expander("Click to view"):
        st.write(extract_important_dates(text))


@st.cache_data(show_spinner="Extracting termination clauses ...")
def termination_clauses(text):
    with st.expander("Click to view"):
        st.write(extract_termination_clauses(text))


@st.cache_data(show_spinner="Extracting obligations ...")
def obligations(text):
    with st.expander("Click to view"):
        st.write(get_obligations(text))


@st.cache_data(show_spinner="Extracting party details ...")
def party_details(text):
    with st.expander("Click to view"):
        st.write(get_party_details(text))


@st.cache_data(show_spinner="Summarizing ...")
def summary(text):
    with st.expander("Click to view"):
        st.write(summarize(text))


@st.cache_data(show_spinner="Classifying ...")
def classify(text):
    with st.expander("Click to view"):
        st.write(
            f"This contract is a type of {classify_contract(text).contract_type.value}"
        )


@st.cache_data(show_spinner="Highlighting ...")
def highlight(text):
    with st.expander("Click to view"):
        st.write(highlight_confidentiality_noncompete(text))


def main():
    st.title("SignSage 🔮📜")

    if st.session_state["dropbox_api_key"] is not None:
        client = DropboxSignClient(st.session_state["dropbox_api_key"])
        requests_list = client.list_signature_requests()
    else:
        st.error("Please enter your API key in the sidebar to continue.")
        st.stop()

    openai.api_key = st.session_state["openai_api_key"]

    # Fetch & Display Signature Requests
    st.subheader("Your Signature Requests")

    st.write(f"You have `{len(requests_list)}` signature requests in total.")

    selected_request = st.selectbox(
        "Choose a contract to review:", requests_list, format_func=lambda x: x["title"]
    )

    # button to run buddy
    submit = st.button("Review")

    if submit:
        col1, col2 = st.columns(2)

        file = client.download_file(selected_request["signature_id"])
        text = get_text("file.pdf")
        with col1:
            st.subheader("Your contract")
            displayPDF(file, 600)

        # Download file
        with col2:
            st.subheader("Classification")
            classify(text)

            st.subheader("Summary")
            summary(text)

            st.subheader("Party Details")
            party_details(text)

            st.subheader("Important Dates")
            important_dates(text)

            st.subheader("Obligations")
            obligations(text)

            st.subheader("Termination clauses")
            termination_clauses(text)

            st.subheader("Confidentiality & Non-compete")
            highlight(text)

            st.subheader("Ready to sign?")
            st.write(f"Click [here]({selected_request['url']}) to sign the document.")


if __name__ == "__main__":
    sidebar()
    main()
