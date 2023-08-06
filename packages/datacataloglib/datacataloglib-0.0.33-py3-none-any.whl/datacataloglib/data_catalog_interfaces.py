from typing import List
import pandas as pd

# addDataSet(..)
# {
#   "dataset": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "description": "patient statistics info",
#       "tags": ["url-to-data", "patient"],
#        "columns": [
#          { "name": "id",
#            "description": "patient id",
#            "type": "int"
#          },
#          { "name": "name",
#            "description": "patient name",
#            "type": "string"
#          },
#          { "name": "age",
#            "description": "patient age",
#            "type": int
#          }
#          { "name": "address",
#            "description": "patient address",
#            "type": "string"
#          }
#        ]
#      }
#    ]
# }


class Dataset(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'description', 'tags', 'columns', 'url']
   def __init__(self, org, project, repository, dataset, description, tags, columns, url=""):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.description = description
            self.tags = tags
            self.columns =columns
            self.url = url
        
def create_addDataset(dataset_list):
    #return {"dataset": dataset_list} if len(dataset_list)>0 else None
    return  dataset_list if len(dataset_list)>0 else None

def create_entry_for_addDataset(
    org, project, repository="project_data", dataset="Image", description="", tags=[], columns=[], url=""
):
    return {
        **({'org': org} if org is not None else {}),
        "project": project,
        "repository": repository,
        "dataset": dataset,
        "description": description,
        "tags": tags,
        "columns": columns,
        "url": url
    }


# {
#   "tableMetadata": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "descriptionSource": "dvc",
#       "tags": ["versions"],
#       "description": "*Version Number:* 2\n*Version Date:* 20Jan2021"
#      }
#    ]
# }


class DatasetVersion(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'description', 'author', 'source', 'tags']
   def __init__(self, org, project, repository, dataset, description, author, source, tags):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.description = description
            self.author = author
            self.source =source
            self.tags = tags
            

def create_addDatasetVersion(tableMetadata_list):
    # return {"tableMetadata": tableMetadata_list} if len(tableMetadata_list)>0 else None
    return tableMetadata_list if len(tableMetadata_list)>0 else None


def create_entry_for_addDataSetVersion(
    org,
    project,
    repository="project_data",
    dataset="Image",
    description="",
    author="",
    source="",
    tags=[]
):
    return {
        **({'org': org} if org is not None else {}),
        "project": project,
        "repository": repository,
        "dataset": dataset,
        "description": description,
        "author": author,
        "source": source,
        "tags": tags
    }


# {
#   "columnStatistics": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "columns": [
#         {
#         "column":"age",
#         "statistics": [
#           {
#             "statName": "distinct values",
#             "statValue": 50,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "min value",
#             "statValue": 7,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "max value",
#             "statValue": 70,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "average",
#             "statValue": 27,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           }
#           ]
#         },
#         {
#           "column":"name",
#           "statistics": [
#             {
#               "statName": "distinct values",
#               "statValue": 25,
#               "startEpoch": 00000000001,
#               "endEpoch": 00000000002
#             }
#             ]
#           }
#         ]
#     }
# }


   
class DatasetStatisticColumn(object):
   __slots__ = ['column', 'statistics']
   def __init__(self, column, statistics):
            self.column = column
            self.statistics = statistics
            

class DatasetStatistic(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'columns']
   def __init__(self, org, project, repository, dataset, columns : List[DatasetStatisticColumn]):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.columns = columns


    

def create_addColumnStatistics(columnStatistics_list):
    #return {"columnStatistics": columnStatistics_list} if len(columnStatistics_list)>0 else None
    return columnStatistics_list if len(columnStatistics_list)>0 else None


def create_entry_for_addColumnStatistics(
    org, project, repository="project_data", dataset="Image", columns=[]
):
    return {
                **({'org': org} if org is not None else {}),
                "project": project,
                "repository": repository,
                "dataset": dataset,
                "columns": columns,
            } if len(columns)>0 else None
        
def add_column_statistic(column_name, statistics):
    return {
        "column": column_name,
        # "statistics": [
        #     {"name": k, "value": f"{v}" }
        #     for k, v in statistics.items()
        #     if not pd.isna(v)
        # ],
        "statistics": [
            row if ('startEpoch' in row) and ('endEpoch' in row) else { **row, "startEpoch": 0,  "endEpoch": 0 } for row in statistics
        ],
    }



class DatasetPipeline(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'branch', 'stages', 'comment', 'author', 'source', 'tags']
   def __init__(self, org, project, repository, dataset, branch, stages, comment, author, source, tags):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.branch = branch
            self.stages = stages
            self.comment = comment
            self.author = author
            self.source = source
            self.tags = tags

def create_addDatasetPipeline(pipelineMetadata_list):
    # return {"tableMetadata": tableMetadata_list} if len(tableMetadata_list)>0 else None
    return pipelineMetadata_list if len(pipelineMetadata_list)>0 else None

def create_entry_for_addDataSetPipeline(
    org,
    project,
    repository="project_data",
    dataset="Image",
    branch="",
    stages={},
    comment="",
    author="",
    source="",
    tags=""
):
    return {
        **({'org': org} if org is not None else {}),
        "project": project,
        "repository": repository,
        "dataset": dataset,
        "branch": branch,
        "stages": stages,
        "comment": comment,
        "author": author,
        "source": source,
        "tags": tags
    }


