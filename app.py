import streamlit as st
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener las credenciales de Azure
clu_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
clu_key = os.getenv("AZURE_LANGUAGE_KEY")
project_name = os.getenv("LU_PROJECT_NAME")
deployment_name = os.getenv("LU_DEPLOYMENT_NAME")

# Crear una instancia del cliente de Azure
client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))

# Función para analizar la consulta
def analyze_query(query):
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "es-es",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )
    return result

# Función para mostrar los resultados
def display_results(result):
    st.write(f"**Query:** {result['result']['query']}")
    
    top_intent = result['result']['prediction']['topIntent']
    st.write(f"**Top Intent:** {top_intent}")
    
    st.write(f"**Category of Top Intent:** {result['result']['prediction']['intents'][0]['category']}")
    st.write(f"**Confidence Score of Top Intent:** {result['result']['prediction']['intents'][0]['confidenceScore']}")
    
    st.write("**Entities:**")
    print(result['result'])
    for entity in result['result']['prediction']['entities']:
        st.write(f"- **Category:** {entity['category']}")
        st.write(f"  **Text:** {entity['text']}")
        st.write(f"  **Confidence Score:** {entity['confidenceScore']}")
        if "resolutions" in entity:
            st.write("  **Resolutions:**")
            for resolution in entity["resolutions"]:
                st.write(f"    - **Kind:** {resolution['resolutionKind']}")
                st.write(f"      **Value:** {resolution['value']}")
        if "extraInformation" in entity:
            st.write("  **Extra Information:**")
            for data in entity["extraInformation"]:
                st.write(f"    - **Kind:** {data['extraInformationKind']}")
                if data["extraInformationKind"] == "ListKey":
                    st.write(f"      **Key:** {data['key']}")
                if data["extraInformationKind"] == "EntitySubtype":
                    st.write(f"      **Value:** {data['value']}")

# Interfaz de Streamlit
st.title("Consulta de intenciones de chatbot para taller de coches")
st.write("Lista de ejemplos de consultas:")
examples = [
    "¿Cuánto cuesta una revisión general?",
    "Necesito cambiar el aceite de mi coche.",
    "Quisiera saber si tienen neumáticos de invierno.",
    "¿Tienen servicio de reparación de frenos?",
    "¿Donde se encuentra el taller?",
    "¿Hacen revisiones para la ITV?"
]

for example in examples:
    st.write(f"- {example}")

query = st.text_input("Introduzca una frase para analizarla:")

if query:
    st.write("Analizando la consulta...")
    result = analyze_query(query)
    display_results(result)
