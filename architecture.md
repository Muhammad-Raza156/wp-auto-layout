```mermaid
graph LR
    subgraph "User Interaction"
        A["User Input (Terminal)"]
    end

    subgraph "Main Workflow (main.py)"
        B("main()")
        C("run_workflow()")
    end

    subgraph "LangGraph Core (graphs/workflow.py)"
        D[StateGraph]
        E["Nodes (Agents)"]
        F["Edges (Flow)"]
        G[ContentCreationState]
    end

    subgraph "Agents (agents/)"
        H[ask_question_agent.py]
        I[human_agent.py]
        J[summary_agent.py]
        K[summary_recap_intent.py]
        L[brand_story_map_agent.py]
        M[page_text_content.py]
        N[image_generation.py]
        O[home_page_agent.py]
    end

    subgraph "Prompts (prompts/)"
        P[brand_story_map_prompt.py]
        Q[home_page_prompt.py]
        R[other prompts]
    end

    subgraph "Language Models (language_models/)"
        S[google_gemini.py]
    end

    subgraph "External Services"
        T[Groq API]
        U[FAL.AI API]
        V[WordPress API]
    end

    subgraph "Utilities (utils.py)"
        W[File I/O]
        X[Image Handling]
        Y[String Manipulation]
    end
    subgraph "Settings (config/settings.py)"
        Z[API Keys]
    end
    subgraph "Data (data/)"
        AA[JSON files]
    end
    subgraph "Output Images (output_images/)"
        AB[Generated images]
    end
    subgraph "Output Files"
        AC[brand_story_map.txt]
        AD[image_generation_output.json]
        AE[893_updated.json]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    E --> H
    E --> I
    E --> J
    E --> K
    E --> L
    E --> M
    E --> N
    E --> O
    E --> P
    E --> Q
    E --> R
    E --> S
    H --> P
    J --> R
    K --> R
    L --> P
    M --> R
    N --> R
    O --> Q
    S --> T
    N --> U
    N --> V
    M --> W
    N --> W
    W --> X
    W --> Y
    C --> Z
    M --> AA
    N --> AB
    L --> AC
    N --> AD
    N --> AE
    style A fill:#ccf,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#cfc,stroke:#333,stroke-width:2px
    style E fill:#cfc,stroke:#333,stroke-width:2px
    style F fill:#cfc,stroke:#333,stroke-width:2px
    style G fill:#cfc,stroke:#333,stroke-width:2px
    style H fill:#fcc,stroke:#333,stroke-width:2px
    style I fill:#fcc,stroke:#333,stroke-width:2px
    style J fill:#fcc,stroke:#333,stroke-width:2px
    style K fill:#fcc,stroke:#333,stroke-width:2px
    style L fill:#fcc,stroke:#333,stroke-width:2px
    style M fill:#fcc,stroke:#333,stroke-width:2px
    style N fill:#fcc,stroke:#333,stroke-width:2px
    style O fill:#fcc,stroke:#333,stroke-width:2px
    style P fill:#cff,stroke:#333,stroke-width:2px
    style Q fill:#cff,stroke:#333,stroke-width:2px
    style R fill:#cff,stroke:#333,stroke-width:2px
    style S fill:#ffc,stroke:#333,stroke-width:2px
    style T fill:#fcf,stroke:#333,stroke-width:2px
    style U fill:#fcf,stroke:#333,stroke-width:2px
    style V fill:#fcf,stroke:#333,stroke-width:2px
    style W fill:#cfc,stroke:#333,stroke-width:2px
    style X fill:#cfc,stroke:#333,stroke-width:2px
    style Y fill:#cfc,stroke:#333,stroke-width:2px
    style Z fill:#cfc,stroke:#333,stroke-width:2px
    style AA fill:#cfc,stroke:#333,stroke-width:2px
    style AB fill:#cfc,stroke:#333,stroke-width:2px
    style AC fill:#cfc,stroke:#333,stroke-width:2px
    style AD fill:#cfc,stroke:#333,stroke-width:2px
    style AE fill:#cfc,stroke:#333,stroke-width:2px
