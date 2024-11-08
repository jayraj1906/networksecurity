from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    try:
        requirementsList:List[str]=[]
        with open('requirements.txt','r') as f:
            lines=f.readlines()
            for line in lines:
                requirements=line.strip()
                if requirements and requirements!='-e .':
                    requirementsList.append(requirements)
    except FileNotFoundError:
        print("Requirements.txt file not found")    

    return requirementsList


setup(
    name="Network Security",
    version="0.0.1",
    author="Jayraj Chaudhary",
    packages=find_packages(),
    install_requires=get_requirements()
)