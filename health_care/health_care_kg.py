import csv
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

AURA_INSTANCENAME = os.environ['AURA_INSTANCENAME']
NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USERNAME = os.environ['NEO4J_USERNAME']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']
NEO4J_DATABASE = os.environ['NEO4J_DATABASE']
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH, database=NEO4J_DATABASE)

# Functino to connect and run a Cypher query
def execute_query(driver, cypher_query, parameters=None):
  try:
    with driver.session(database=NEO4J_DATABASE) as session:
      result = session.run(cypher_query, parameters)
      return result
  except Exception as e:
    print(f'Error: {e}')
  finally:
    driver.close()

# Functino to create healthcare provider nodes
def create_healthcare_provider_node(driver, provider, bio):
  print('Creating healthcare provider node...')
  create_provider_query = """
    MERGE (hp:HealthcareProvider {name: $provider, bio: $bio})
  """
  parameters = {'provider': provider, 'bio': bio}
  execute_query(driver, create_provider_query, parameters)
  
# Function to create patient nodes
def create_patient_node(driver, patient, patient_age, patient_gender, patient_condition):
  print('Creating patient node...')
  create_patient_query = """
    MERGE (p:Patient {name: $patient, age: $patient_age, gender: $patient_gender, condition: $patient_condition})
  """
  parameters = {'patient': patient, 'patient_age': patient_age, 'patient_gender': patient_gender, 'patient_condition': patient_condition}
  execute_query(driver, create_patient_query, parameters)
  
# Function to create specialization nodes
def create_specialization_node(driver, specialization):
  print('Creating specialization node...')
  create_specialization_query = """
    MERGE (s:Specialization {name: $specialization})
  """
  parameters = {'specialization': specialization}
  execute_query(driver, create_specialization_query, parameters)

# Function to create location nodes
def create_location_node(driver, location):
  print('Creating location node...')
  create_location_query = """
    MERGE (l:Location {name: $location})
  """
  parameters = {'location': location}
  execute_query(driver, create_location_query, parameters)

# Function to create relationships
def create_relationships(driver, provider, patient, specialization, location):
  print('Creating relationships...')
  create_relationship_query = """
    MATCH (hp:HealthcareProvider {name: $provider}), (p:Patient {name: $patient})
    MERGE (hp)-[:TREATS]->(p)
    WITH hp
    MATCH (hp), (s:Specialization {name: $specialization})
    MATCH (hp)-[:SPECIALIZES_IN]->(s)
    WITH hp
    MATCH (hp), (l:Location {name: $location})
    MERGE (hp)-[:LOCATED_AT]->(l)
  """
  parameters = {'provider': provider, 'patient': patient, 'specialization': specialization, 'location': location}
  execute_query(driver, create_relationship_query, parameters)

# Function to read the CSV file and populate the graph
def main():
  driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH, database=NEO4J_DATABASE)
  
  with open('./health_care/healthcare.csv', 'r') as file:
    reader = csv.DictReader(file)
    print('Reading healthcare.csv...')
    
    for row in reader:
      provider = row['Provider']
      patient = row['Patient']
      specialization = row['Specialization']
      location = row['Location']
      bio = row['Bio']
      patient_age = row['Patient_Age']
      patient_gender = row['Patient_Gender']
      patient_condition = row['Patient_Condition']
      
      create_healthcare_provider_node(driver, provider, bio)
      create_patient_node(driver, patient, patient_age, patient_gender, patient_condition)
      create_specialization_node(driver, specialization)
      create_location_node(driver, location)
      create_relationships(driver, provider, patient, specialization, location)
  driver.close()
  print('Graph populated successfully!')
  
if __name__ == '__main__':
  main()