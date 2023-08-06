from datacataloglib.data_catalog_interfaces import create_addDataset, create_entry_for_addDataset,  Dataset , DatasetVersion, create_entry_for_addDataSetVersion, create_addDatasetVersion, DatasetStatistic, DatasetStatisticColumn, create_addColumnStatistics, create_entry_for_addColumnStatistics, add_column_statistic
from datacataloglib.data_catalog_interfaces import DatasetPipeline, create_addDatasetPipeline, create_entry_for_addDataSetPipeline
from datacataloglib.request_helper import request_post_if_has_value

from typing import List


"""
example: dataset = Dataset("org", "project", "repository", "dataset", "description", tags=[], columns=[])
"""
def addDataset(url, dataset_list : List[Dataset], extra={}):

    return request_post_if_has_value(
        f"{url}",
        json=create_addDataset(
            [
                create_entry_for_addDataset(
                    item.org,
                    item.project,
                    item.repository,
                    item.dataset,
                    item.description,
                    tags=item.tags,
                    columns=item.columns,
                    url= item.url
                )  for item in dataset_list
            ]
        )
        ,extra=extra
    )
        
# addDataset("url", [Dataset("org", "project", "repository", "dataset", "description", tags=["url-to-data"], columns=[{"name":"something", "description": "again", "type": "int64"}])])


def addDatasetVersion(url,dataset_version_list: List[DatasetVersion], extra={}):
        return request_post_if_has_value(
        f"{url}",
        json=create_addDatasetVersion([
            create_entry_for_addDataSetVersion(
                item.org,
                item.project,
                item.repository,
                item.dataset,
                item.description,
                item.author,
                item.source,
                tags=item.tags
            )
            for item in dataset_version_list
        ]), extra=extra)
        

#addDatasetVersion("url",[DatasetVersion("org", "project", "repository", "dataset", "description", "author", "source", tags=["versions"])])
    
        
             
             
def addDatasetStatistic(url, dataset_statistic_list: List[DatasetStatistic], extra={}):  
              
            return request_post_if_has_value(
                f"{url}",
                json=create_addColumnStatistics([
                create_entry_for_addColumnStatistics(
                    item.org,
                    item.project,
                    item.repository,
                    item.dataset,
                    columns=[
                        add_column_statistic(each_column.column, each_column.statistics)
                        for each_column in item.columns
                    ],
                )
                for item in dataset_statistic_list
            ]), extra=extra)

# addDatasetStatistic("url",[DatasetStatistic("org","project", "repository", "dataset", 
#                                       [ DatasetStatisticColumn("column_name", [{ "name": "distinct values", "value": 50} )] ]
#                                       )])


def addDatasetPipeline(url, dataset_pipeline_list: List[DatasetPipeline], extra={}):
    return request_post_if_has_value(
        f"{url}",
        json=create_addDatasetPipeline([
            create_entry_for_addDataSetPipeline(
                item.org,
                item.project,
                item.repository,
                item.dataset,
                item.branch,
                item.stages,
                item.comment,
                item.author,
                item.source,
                tags=item.tags
            )
            for item in dataset_pipeline_list
        ]), extra=extra)