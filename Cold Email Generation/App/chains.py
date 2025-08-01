import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,
                            groq_api_key=os.getenv("GROQ_API_KEY"),
                            model_name="llama-3.3-70b-versatile")

        def extract_jobs(self, cleaned_text):
            prompt_extract = PromptTemplate.from_template(
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):
                """
            )
            chain_extract = prompt_extract | self.llm
            res = chain_extract.invoke(input={"page_data": cleaned_text})
            try:
                json_parser = JsonOutputParser()
                res = json_parser.parse(res.content)
            except OutputParserException:
                raise OutputParserException("Context too big. Unable to parse jobs.")
            return res if isinstance(res, list) else [res]

        def write_mail(self, job, links):
            prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION:
                {job_description}
        
                ### INSTRUCTION:
                You are Aditi, pursued M.Tech CSE with specialization in Data Science from NIT Surat. You've passed out in 25th June 2025.
	            You did dissertation project on 'Enhancing Fake Reviews Detection via Transformers and MetaData. A paper based on this
	            has been submitted to icSoftComp 2025, under Springer Nature. You also did project on web scrapping. Your B.Tech project
	            was on 'Securing Surveillance Images for IoT Devices' which implemented the concept of Image Steganography. You also have 
	            knowledge on Python, SQL, NLP,LLMs, Machine Learning, Deep Learning, Transformers.

	            Now draft a cold mail based on the given information and the job description. 
        
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
        
                """
            )
            chain_email = prompt_email | self.llm
            res = chain_email.invoke({"job_description": str(job), "link_list": links})
            return res.content

if __name__=="__main__":
    print(os.getenv("GROQ_API_KEY"))