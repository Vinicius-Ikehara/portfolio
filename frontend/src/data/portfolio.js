// All portfolio data hardcoded here
// Update this file and redeploy to change content

export const profile = {
  name: "Vinicius Ikehara",
  title: "AI Developer",
  bio: "As an AI Developer, I build advanced, scalable solutions powered by Large Language Models, turning complex business challenges into intelligent, automated systems. My expertise lies in designing high-performance automations, conversational agents, and RAG architectures that connect LLMs to real organizational data with accuracy, reliability, and strategic intent.",
  email: "vhikehara@gmail.com",
  phone: "+55 (11) 95151-7465",
  location: "Rio Paranaiba ,MG",
  avatar_url: "https://media.licdn.com/dms/image/v2/D4D03AQGRwrqzxMP2fw/profile-displayphoto-crop_800_800/B4DZqe4rXFJcAI-/0/1763602250834?e=1765411200&v=beta&t=OXwhUa8DdV6AQj9hLz3DvGsKu-AQOpWhx5On5XAZ648",
  skills: [
    "n8n",
    "AI",
    "LLM",
    "Prompt Engineering",
    "RAG",
    "SQL",
    "Vector Search"
  ],
  social_links: {
    GitHub: "https://github.com/Vinicius-Ikehara",
    LinkedIn: "https://www.linkedin.com/in/vinicius-ikehara/"
  }
}

export const experiences = [
  {
    id: 1,
    position: "AI Developer",
    company: "domy",
    description: "Working on large-scale AI systems powered by massive datasets, contributing to the full development lifecycle of custom applications. Core focus on designing and implementing advanced AI components. Developed pipelines that transform large volumes of data into actionable insights, delivering automated interactions to clients through high-volume WhatsApp workflows orchestrated via n8n. Built an internal RAG and vector search system that allows employees to instantly retrieve information from documents, PDFs, files, and structured database content.",
    technologies: ["Python", "n8n", "Apache Airflow", "Agno", "Vector Databases", "RAG", "LLM", "WhatsApp API"],
    start_date: "2025-08",
    end_date: null,
    current: true
  },
  {
    id: 2,
    position: "Data Analyst & AI",
    company: "HSystem",
    description: "Supported team by collecting, cleaning, and interpreting data to provide actionable insights and drive informed decision-making. Integrated Artificial Intelligence into processes to enhance automation and analytical capabilities through LLMs. Developed ETL pipelines using n8n, AWS Lambda, and Python. Designed and maintained interactive dashboards with Power BI and Metabase. Implemented Retrieval-Augmented Generation (RAG) solutions using vector databases and semantic search.",
    technologies: ["Python", "n8n", "AWS Lambda", "Power BI", "Metabase", "MySQL", "MongoDB", "LLM", "RAG", "Vector Database", "Docker"],
    start_date: "2024-05",
    end_date: "2025-08",
    current: false
  },
  {
    id: 3,
    position: "Junior Data Analyst",
    company: "Banco Daycoval",
    description: "Supported team by collecting, cleaning, and interpreting data to provide actionable insights and drive informed decision-making. Developed ETL pipelines using SQL Server Integration Services (SSIS). Created RPA's (Robotic Process Automation) with Python. Designed applications on Microsoft Access and implemented interactive dashboards with Tableau.",
    technologies: ["Python", "PyAutoGUI", "Selenium", "Pandas", "SQL Server", "SSIS", "Tableau", "Microsoft Access", "VBA"],
    start_date: "2023-01",
    end_date: "2024-05",
    current: false
  }
]

export const projects = [
  {
    id: 1,
    title: "Pokédex AI Agent",
    description: "This project is an AI-powered chatbot that answers questions about the first generation of Pokémon. Built on n8n with a PostgreSQL vector database and GPT-4o mini, it supports semantic search and delivers accurate, conversational responses. Try it out now!",
    technologies: ["n8n", "PostgreSQL", "Vector Database", "RAG", "GPT-4o mini", "Webhook", "Semantic Search"],
    image_url: null,
    project_url: "/projects/pokedex",
    github_url: null,
    slug: "pokedex",
    interactive: true
  }
]
