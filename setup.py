from setuptools import setup, find_packages

setup(
    name="mental-health-assistant",
    version="0.1.0",
    description="Asistente de salud mental basado en LLMs con API de GroqCloud",
    author="Tu nombre",
    author_email="tu@email.com",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "requests>=2.25.0",
        "gradio>=3.32.0",
        "pillow>=9.0.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        'console_scripts': [
            'mental-health-assistant=src.main:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)