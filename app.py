import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()
from utils import utils

# Setup your config
utils.page_config()
utils.style_app()

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("PRD Generator")
st.markdown("### Welcome to the PRD Generator by Lyzr!")
st.markdown("PRD Generator generate a structured PRD tailored to your project's needs, considering various aspects essential for successful product development !!!")



# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

data = "data"
os.makedirs(data, exist_ok=True)


open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def prd_generator(product, purpose):
    
    project_manager = Agent(
        prompt_persona="""You are an expert Experienced product manager adept at crafting comprehensive Product Requirements Documents (PRDs) that meticulously outline project scope, features, and functionalities. Skilled in translating stakeholder requirements into actionable plans to drive successful product development.""",
        role="AI PRD Generator", 
    )

    project_report_doc =  Task(
        name="Project Report Document",
        agent=project_manager,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the description provided, Could you help me draft a Product Requirements Document (PRD) for a new project? We're developing a {product}. The aim is to {purpose}. We need to outline all the necessary features, functionalities, and requirements for this project. Can you assist in creating a comprehensive PRD, covering aspects such as scope, user stories, functional and non-functional requirements, design guidelines, assumptions, constraints, dependencies, and acceptance criteria? Please make sure to include any relevant details and prioritize the features based on their importance. Additionally, consider any potential challenges or risks we might encounter during the development process.",
        log_output=True,
        enhance_prompt=False,
        default_input=product
    )


    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="AI PRD Generator",
        completion_message="App Generated all things!",
        tasks=[
            project_report_doc,
            
        ],
    ).run()

    return main_output



if __name__ == "__main__":
    product = st.text_area('Brief description of the product')
    purpose = st.text_area('State the purpose')


    if (product and purpose) != '':
        if st.button('Submit'):
            generated_output = prd_generator(product=product, purpose=purpose)
            output = generated_output[0]['task_output']
            st.subheader('Generated PRD')
            st.write(output)
    else:
        st.warning('Product and Purpose are not provided')

    utils.template_end()
