from dotenv import load_dotenv
import os
from langchain_community.graphs import Neo4jGraph

load_dotenv()

AURA_INSTANCENAME = os.environ['AURA_INSTANCENAME']
NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USERNAME = os.environ['NEO4J_USERNAME']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']
NEO4J_DATABASE = os.environ['NEO4J_DATABASE']
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

kg = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE)

cypher = """
  MATCH (n) RETURN count(n) as numberOfNodes
"""

result = kg.query(cypher)
print(f"There are {result[0]['numberOfNodes']} nodes.")

# Match only the Providers nodes by specifying the node label
cypher_provider = """
  MATCH (n:HealthcareProvider)
  RETURN count(n) as numberOfProviders
"""
result = kg.query(cypher_provider)
print(f"There are {result[0]['numberOfProviders']} Healthcare Providers.")

# return the names of the Healthcare Providers
cypher_provider_names = """
  MATCH (n:HealthcareProvider)
  RETURN n.name as ProviderName
"""
result = kg.query(cypher_provider_names)
print("Healthcare Providers:")
for r in result:
  print(f"  {r['ProviderName']}")

# list all patients in the graph
cypher_patients = """
  MATCH (n:Patient)
  RETURN n.name as PatientName
"""
result = kg.query(cypher_patients)
print("Patients:")
for r in result:
  print(f"  {r['PatientName']}")
  
# list all Locations in the graph
cypher_locations = """
  MATCH (n:Location)
  RETURN n.name as LocationName
"""
result = kg.query(cypher_locations)
print("Locations:")
for r in result:
  print(f"  {r['LocationName']}")

# list all patients treated by a specific provider
cypher_patients_by_provider = """
  MATCH (hp:HealthcareProvider {name: 'Dr. John Smith'})-[:TREATS]->(p:Patient)
  RETURN p.name as PatientName
"""
result = kg.query(cypher_patients_by_provider)
print("Patients treated by Dr. John Smith:")
for r in result:
  print(f"  {r['PatientName']}")