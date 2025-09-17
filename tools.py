## https://serper.dev/

from dotenv import load_dotenv
load_dotenv()
import os

os.environ['SERPER_API_KEY'] = 'e0f4962d9e523cf77248bfffcfcde189c7554bae'


from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()