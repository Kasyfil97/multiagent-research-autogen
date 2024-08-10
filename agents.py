import autogen
import os
from config import Config
os.environ["AUTOGEN_USE_DOCKER"] = "0"

config = Config.load_yaml()
gpt4_config = config.gpt4_config



user = autogen.UserProxyAgent(
    name="user",
    system_message="Interact with the manager to discuss the plan.",
    code_execution_config=False,
)

manager = autogen.AssistantAgent(
    name="manager",
    system_message="""Receive user request, and Understand it. If the user request is complex needing more than one member, you should make a plan to execute the request, and assign the task to the member: researcher, analyst, and spokesman. But if the request is simple, you could assign the task directly to the member. You are not allow to answer the user request directly, you should assign the task to the spokesman.
    If you need feedback from user, you should ask spokesman to ask the feedback from user.
    If user say ok, you should response "TERMINATE"
    """,
    description='A manager. The task are making a plan, assign the task to the member.',
    llm_config=gpt4_config,
)

researcher = autogen.AssistantAgent(
    name="researcher",
    system_message="""You follow the plan from the project manager. 
    Your task are doing web browsing by google search and/or by google map, find the appropriate data from the web, and scrap it. 
    You must make sure the scrapping data is correct based on the user request.
    give the result to the analyst.
    If you need feedback from user, you should ask spokesman to ask the feedback from user.
    """,
    description='A researcher. The task are doing web browsing by google search and/or by google map, find the appropriate data from the web, and scrap it.',
    llm_config=gpt4_config,
)

analyst = autogen.AssistantAgent(
    name="analyst",
    system_message="""You follow the plan from the manager. 
    Your task are just analizing result from the researcher on the user request, and make the summary from all your analysis
    You should give the summary to the spokesman to ask user's feedback, if the result is not correct, you should revise the result.
    You should check the result from the researcher, if the result is not correct, you should give feedback to the researcher. 
    If you need more data, you could ask researcher to get data by doing web browsing or web scrapping.
    But if they can't get the data, you just make the summary based on the data you have.
    If you need feedback from user, you should ask spokesman to ask the feedback from user.
    """,
    description='A analyst. The task are just analizing result from the researcher on the user request, and make the summary from all your analysis',
    llm_config=gpt4_config,
)

programmer = autogen.AssistantAgent(
    name="programmer",
    llm_config=gpt4_config,
    system_message="""You write python/shell code based on the plan or analyst request.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    If you need feedback from user, you should ask spokesman to ask the feedback from user.
""",
    description='A programmer. The task are writing python/shell code based on the plan or analyst request'
)

spokesman = autogen.AssistantAgent(
    name="spokesman",
    system_message="""You follow plan from manager. Your task are: 
    1/Report the analysis summary from analys to the user. After that, Ask user feedback, if user feedback ok, response "TERMINATE"
    2/if manager or researcher or analyst or programmer need feedback from user, you should ask the feedback from user, and give the feedback to them.
    3/Please report in indonesia language
    """,
    llm_config=gpt4_config,
    description='A spokesman. The task are reporting the analysis summary from analys to the user, ask user feedback, and give feedback to the member if needed.'
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the web browsing google map, and web scrapping",
    human_input_mode="NEVER"# Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

coder = autogen.UserProxyAgent(
    name="Coder",
    system_message="Coder. Execute the code written by programmer",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "D:/research agent",
        "use_docker": False,}
        )