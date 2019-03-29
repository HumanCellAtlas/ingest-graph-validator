import json, os, ingestapi
from py2neo import Graph, authenticate


def makeEntityGraph(submission, entityType, nodeType, entities):
    content = {}
    content[entityType] = []
    for index, entity in enumerate(entities):
        content[entityType].append(entity)

    query = """
    WITH {submission} AS envelope, {content} AS es
    UNWIND es.""" + entityType + """ AS entity
    MERGE (se:SubmissionEnvelope {id: envelope.uuid.uuid})
    ON CREATE SET se.uuid = envelope.uuid.uuid, se.submissionDate = envelope.submissionDate
    MERGE (e:""" + nodeType + """ {id: entity.uuid.uuid})
    ON CREATE SET e.uuid = entity.uuid.uuid, e.displayName = entity.content.id
    MERGE (se)-[:CONTAINS]->(e)
    """

    # Send Cypher query.
    print """Running: """ + query
    graph.run(query, submission=submission, content=content).dump()


def addRelatedEntities(source, sourceType, targets, targetType, property):
    content = []
    for index, _target in enumerate(targets):
        content.append(_target)

    if content:
        query = """
        WITH {sourceData} AS source, {targetData} AS targets 
        UNWIND targets AS target
        MERGE (s:""" + sourceType + """ {id: source.uuid.uuid})
        MERGE (t:""" + targetType + """ {id: target.uuid.uuid})
        MERGE (s)-[:""" + property + """]->(t)
        """

        # Send Cypher query.
        print """Running: """ + query
        graph.run(query, sourceData=source, targetData=content).dump()


DEFAULT_INGEST_URL=os.environ.get('INGEST_API', 'http://api.ingest.staging.data.humancellatlas.org')
ingest_api = ingestapi.IngestApi(DEFAULT_INGEST_URL)

# create neo graph
authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph()

# grab submission envelopes
subs = {}
try:
    subs['submissionEnvelopes'] = ingest_api.getSubmissions()
except Exception, e:
    flash("Can't connect to ingest API!!", "alert-danger")

for sub in subs['submissionEnvelopes']:
    subs_url = sub['_links']['self']['href']

    a = ingest_api.getEntities(subs_url, "analyses")
    makeEntityGraph(sub, 'analyses', 'Analysis', a)

    a1 = ingest_api.getEntities(subs_url, "assays")
    makeEntityGraph(sub, 'assays', 'Assay', a1)

    f = ingest_api.getEntities(subs_url, "files")
    makeEntityGraph(sub, 'files', 'File', f)

    p = ingest_api.getEntities(subs_url, "projects")
    makeEntityGraph(sub, 'projects', 'Project', p)

    p1 = ingest_api.getEntities(subs_url, "protocols")
    makeEntityGraph(sub, 'protocols', 'Protocol', p1)

    s = ingest_api.getEntities(subs_url, "samples")
    makeEntityGraph(sub, 'samples', 'Sample', s)

    _analyses = {}
    _analyses = ingest_api.getAnalyses(subs_url)
    for index, _analysis in enumerate(_analyses):
        related = ingest_api.getRelatedEntities('files', _analysis, 'files')
        addRelatedEntities(_analysis, 'Analysis', related, 'File', 'GENERATED')
        related = ingest_api.getRelatedEntities('projects', _analysis, 'projects')
        addRelatedEntities(_analysis, 'Analysis', related, 'Project', 'PART_OF')

    _assays = {}
    _assays = ingest_api.getAssays(subs_url)
    for index, _assay in enumerate(_assays):
        related = ingest_api.getRelatedEntities('files', _assay, 'files')
        addRelatedEntities(_assay, 'Assay', related, 'File', 'GENERATED')
        related = ingest_api.getRelatedEntities('projects', _assay, 'projects')
        addRelatedEntities(_assay, 'Assay', related, 'Project', 'PART_OF')
        related = ingest_api.getRelatedEntities('samples', _assay, 'samples')
        addRelatedEntities(_assay, 'Assay', related, 'Sample', 'DERIVED_FROM')
        related = ingest_api.getRelatedEntities('protocols', _assay, 'protocols')
        addRelatedEntities(_assay, 'Assay', related, 'Protocol', 'PRODUCED_BY')

    _samples = {}
    _samples = ingest_api.getEntities(subs_url, "samples")
    for index, _samples in enumerate(_samples):
        related = ingest_api.getRelatedEntities('derivedFromSamples', _samples, 'samples')
        addRelatedEntities(_samples, 'Sample', related, 'Sample', 'DERIVED_FROM')
        related = ingest_api.getRelatedEntities('projects', _samples, 'projects')
        addRelatedEntities(_samples, 'Sample', related, 'Project', 'PART_OF')
