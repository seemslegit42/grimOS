from setuptools import setup, find_packages

setup(
    name="grimos-shared",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.24.0",
        "passlib>=1.7.4",
        "python-jose>=3.3.0",
        "python-multipart>=0.0.6",
    ],
    author="BitBrew Inc.",
    author_email="dev@bitbrew.ai",
    description="Shared utilities for grimOS backend services",
    keywords="grimos, utilities, backend",
    python_requires=">=3.11",
)