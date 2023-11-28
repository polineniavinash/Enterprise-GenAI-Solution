import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv

load_dotenv()

# Function to get response from LLM
def getLLMResponse(query, kind_option, task_type):
    llm = OpenAI(temperature=.9, model="gpt-3.5-turbo-instruct")
    

    if kind_option=="Intern": # Aspiring and Eager Intern
        examples = [
            {
                "query": "What strategies should I focus on to maximize learning during my internship?",
                "answer": "To maximize learning, engage actively, seek feedback, and work on diverse projects. Embrace tasks and ask questions. Network with colleagues and mentors for insights and document your learnings for continuous growth."
            },
            {
                "query": "How can I make a lasting impression during my internship?",
                "answer": "Make a lasting impression by showing initiative, delivering quality work, being proactive in problem-solving, demonstrating a positive attitude, and building strong relationships with colleagues and mentors."
            },
            {
                "query": "What skills should I focus on developing as an intern in tech?",
                "answer": "Focus on developing technical skills relevant to your field, soft skills like communication and teamwork, and a deep understanding of industry trends and best practices."
            },
            {
                "query": "How do I handle challenging tasks as an intern?",
                "answer": "Handle challenging tasks by breaking them down into manageable steps, seeking guidance when needed, staying organized, maintaining a learning mindset, and leveraging resources and teamwork."
            }
        ]

    elif kind_option=="Senior Engineer": # Experienced and Knowledgeable Senior Engineer
        examples = [
            {
                "query": "How can we improve code efficiency in large-scale software projects?",
                "answer": "For code efficiency, write clean, readable code, implement robust testing, leverage design patterns, optimize data structures and algorithms, and regularly review and refactor code for scalability."
            },
             {
                "query": "How do I mentor junior engineers effectively?",
                "answer": "Mentor effectively by sharing your experience, providing constructive feedback, setting clear goals, being accessible, encouraging questions, and fostering a supportive and inclusive environment."
            },
            {
                "query": "What's the key to managing technical debt in software projects?",
                "answer": "Manage technical debt by prioritizing critical issues, documenting debt for transparency, allocating regular time for refactoring, and balancing short-term fixes with long-term solutions."
            },
            {
                "query": "How can I stay updated with the latest technologies in software engineering?",
                "answer": "Stay updated by reading industry publications, attending workshops and conferences, participating in professional networks, experimenting with new tools and techniques, and continuous learning."
            }
        ]

    elif kind_option=="ML Expert": # Innovative and Insightful ML Expert
        examples = [
            {
                "query": "What are the best practices for deploying machine learning models in production?",
                "answer": "Deploy ML models by testing robustly, monitoring continuously, updating iteratively, ensuring scalability, implementing A/B testing, using version control, prioritizing interpretability, and updating based on feedback."
            },
            {
                "query": "What are the emerging trends in machine learning I should be aware of?",
                "answer": "Stay informed about trends like AI ethics, explainable AI, advancements in deep learning, the integration of AI with IoT, and the increasing use of reinforcement learning in various industries."
            },
            {
                "query": "How do I ensure the ethical use of AI and machine learning in my projects?",
                "answer": "Ensure ethical AI by implementing transparent and accountable AI systems, prioritizing privacy and data security, avoiding biases in datasets, and promoting fairness and inclusivity in AI solutions."
            },
            {
                "query": "What are effective ways to optimize machine learning models for production?",
                "answer": "Optimize ML models for production by fine-tuning hyperparameters, selecting appropriate model architectures, ensuring data quality, and employing techniques like model compression and efficient hardware utilization."
            }
        ]

    elif kind_option=="Product Manager": # Strategic and Visionary Product Manager
        examples = [
            {
                "query": "How can I effectively align product development with market needs?",
                "answer": "Align development with market needs through thorough research, developing user personas, fostering a customer-centric approach, implementing agile methodologies, gathering user feedback, and communicating transparently with stakeholders."
            },
            {
                "query": "How can I foster innovation within my product team?",
                "answer": "Foster innovation by encouraging creativity, experimenting with new ideas, creating a safe environment for risk-taking, promoting cross-functional collaboration, and staying attuned to customer feedback and market trends."
            },
            {
                "query": "What are effective strategies for managing a remote product team?",
                "answer": "Manage a remote team by establishing clear communication channels, setting well-defined goals, using collaborative tools effectively, fostering team bonding, and ensuring flexibility and support for different work environments."
            },
            {
                "query": "How do I balance user needs with business objectives in product development?",
                "answer": "Balance user needs and business objectives by understanding user pain points, aligning product features with business goals, continuously validating ideas with users, and making data-driven decisions."
            }
        ]

    example_template = "Question: {query}\nResponse: {answer}"

    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template
    )

    prefix = """ You are an AI designed for {template_kind_option}, focusing on {template_task_type} tasks.
    Here are some examples: 
    """
    suffix = """ 
    Question: {template_userInput}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )

    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["template_userInput", "template_kind_option", "template_task_type"],
        example_separator="\n"
    )
    #print(new_prompt_template.format(template_userInput=query, template_kind_option=kind_option, template_task_type=task_type))
    response = llm(new_prompt_template.format(template_userInput=query, template_kind_option=kind_option, template_task_type=task_type))
    return response

# UI Configuration
st.set_page_config(page_title="Enterprise AI Solutions by Avinash Polineni",
                   page_icon='🌐',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title("Enterprise AI Solutions by Avinash Polineni")

st.markdown("## Discover AI-Driven Solutions for Business")

# Example use case display
st.markdown("""
### Example Query:
**Question**: How can AI be leveraged to improve customer service in telecom industries?

**Response**: AI can significantly enhance customer service in telecom industries by implementing advanced chatbots for instant query resolution, predictive analytics for personalized service offerings, and automated systems for efficient complaint management. It also aids in sentiment analysis to gauge customer satisfaction and tailor services accordingly.

*Try asking something similar or explore other topics!*
""")

with st.sidebar:
    st.image("brand_logo.png", width=300)  
    st.caption("Created by Avinash Polineni")

form_input = st.text_area('Enter your query', height=150)

kind_option = st.selectbox(
    'Choose your profile:',
    ('Intern', 'Senior Engineer', 'ML Expert', 'Product Manager'), key='kindoption')

task_type = st.selectbox(
    'Select the enterprise application:',
    ('Supply Chain Optimization', 'Customer Service Enhancement', 'Market Analysis', 'Financial Forecasting'), key='tasktype')


submit = st.button("Generate Insights")

if submit:
    with st.spinner('Generating response...'):
        response = getLLMResponse(form_input, kind_option, task_type)
        st.markdown("### AI Generated Insights")
        st.write(response)

# Additional Resources
st.sidebar.markdown("### Additional Resources")
st.sidebar.markdown("[Checkout Avinash's Hugging Face Profile](https://huggingface.co/AvinashPolineni)")
st.sidebar.markdown("[Checkout Avinash's GitHub Profile](https://github.com/polineniavinash)")
st.sidebar.markdown("[Contact Me on LinkedIn](https://linkedin.com/in/avinash-polineni/)")

# Footer
st.markdown("---")
st.caption("© 2023 Avinash Polineni. All Rights Reserved.")
