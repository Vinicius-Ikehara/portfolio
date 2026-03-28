// All portfolio data hardcoded here
// Update this file and redeploy to change content

export const profile = {
  name: "Vinicius Ikehara",
  title: "AI Developer",
  bio: "As an AI Developer, I build advanced, scalable solutions powered by Large Language Models, turning complex business challenges into intelligent, automated systems. My expertise lies in designing high-performance automations, conversational agents, and RAG architectures that connect LLMs to real organizational data with accuracy, reliability, and strategic intent.",
  email: "vhikehara@gmail.com",
  phone: "+55 (11) 95151-7465",
  location: "Rio Paranaiba ,MG",
  avatar_url: "/images/perfil.png",
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
    description: "An AI-powered Pokédex chatbot built with Python, FastAPI, and the Agno AI framework. Features a complete RAG pipeline with Supabase pgvector for semantic search, guardrails for jailbreak protection, and session-based memory. The agent retrieves Pokémon data through embeddings and generates contextualized responses about Gen 1 Pokémon with stats, abilities, evolutions, and images.",
    technologies: ["Python", "FastAPI", "Agno", "Supabase", "pgvector", "RAG", "GPT-5.2", "OpenAI Embeddings", "Guardrails"],
    image_url: null,
    project_url: "/projects/pokedex",
    github_url: null,
    slug: "pokedex",
    interactive: true
  },
  {
    id: 2,
    title: "Dialogflow Virtual Assistant",
    description: "This project is a conversational chatbot built with Google's Dialogflow CX in just a few hours to explore NLP technology. Integrated directly into my portfolio, it uses natural language understanding to answer questions about my professional experience, skills, and projects through custom intent recognition. Try it out now!",
    technologies: ["Dialogflow CX", "Natural Language Processing", "Intent Recognition", "Chatbot", "Google Cloud"],
    image_url: "/images/dialogflow.jpg",
    project_url: "open-chat",
    github_url: null,
    slug: "dialogflow-assistant",
    interactive: true
  },
  {
    id: 3,
    title: "AI Ops Dashboard",
    description: "A real-time observability dashboard that pulls production metrics from Langfuse, showing AI traces, token usage, costs, and latency. Demonstrates end-to-end LLM monitoring with OpenTelemetry auto-instrumentation, self-hosted Langfuse, and a custom Vue.js frontend.",
    technologies: ["Vue.js", "FastAPI", "Langfuse", "OpenTelemetry", "OpenLIT", "LLM Observability"],
    image_url: null,
    project_url: "/projects/ai-ops",
    github_url: null,
    slug: "ai-ops",
    interactive: true
  },
  {
    id: 4,
    title: "Highway Accidents H3",
    description: "Geospatial analysis of Brazilian federal highway accidents using Uber's H3 hexagonal indexing and ClickHouse. Features an interactive heatmap with H3 hexagons rendered on MapLibre GL, real-time aggregations from ClickHouse's native H3 functions, and analytical dashboards revealing accident hotspots, lethality patterns, and temporal trends from PRF open data.",
    technologies: ["ClickHouse", "H3", "MapLibre GL", "Vue.js", "FastAPI", "Geospatial", "Open Data"],
    image_url: null,
    project_url: "/projects/acidentes-h3",
    github_url: null,
    slug: "acidentes-h3",
    interactive: true
  }
]
