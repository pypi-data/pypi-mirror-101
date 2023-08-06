"""
This module contains methods that will be applied inside of the apply call on the freshly convertet
Spark DF that is now as list of dicts.

These methods are meant to be applied in the internal calls of the metadata extraction.
They expect dictionaries which represent the metadata field extracted from Spark NLP annotators.


"""
import numpy as np
import pandas as pd
def meta_extract_language_classifier_max_confidence(row,configs):
    ''' Extract the language classificationw ith highest confidence and drop the others '''
    # Get the best, but what about TOP K! todo
    # TODO conditional sentence extraction and mroe docs
    #unpack all confidences to float and set 'sentence' key value to -1 so it does not affect finding the highest cnfidence
    unpack_dict_values = lambda x : -1 if 'sentence' in x[0]  else float(x[1][0])
    l = list(map(unpack_dict_values,row.items()))
    m = np.argmax(l)
    k = list(row.keys())[m]

    return {k+'_confidence' : row[k][0]} # remoe [0] for list return


def extract_maximum_confidence(row, configs):
    ''' Extract the maximum confidence from any classifier with N classes.
    A classifier with N classes, has N confidences in it's metadata by default, which is too much data usually.
    This extractor gets the highest confidence from the array of confidences.
    This method assumes all keys in metadata corrospond to confidences, except the `sentence` key, which maps to a sentence ID
    key schema is 'meta_' + configs.output_col_prefix + '_confidence'

    Parameters
    -------------
    configs : SparkNLPExtractorConfig
    if configs.get_sentence_origin is True, the sentence origin column will be kept, otherwise dropped.
    row : dict
        i.e. looks like{'meta_category_sentence': ['0'],'meta_category_surprise': ['0.0050183665'],'meta_category_sadness': ['8.706827E-5'],'meta_category_joy': ['0.9947379'],'meta_category_fear': ['1.5667251E-4']}
    Returns
    ------------
    dict
      if configs.get_sentence_origin True  {'meta_sentiment_dl_sentence': ['0', '1'], 'meta_sentiment_dl_confidence': [0.9366506, 0.9366506]}
      else {'meta_sentiment_dl_confidence': [0.9366506, 0.9366506]}
    '''
    meta_sent_key = 'meta_' + configs.output_col_prefix + '_sentence'
    fl = lambda k : False if 'sentence' in k else True
    confidences_keys = filter (fl, row.keys())

    if configs.pop_meta_list :
        return {
            **{'meta_' + configs.output_col_prefix + '_confidence':max([float(row[k][0]) for k in confidences_keys ])},
            **({'meta_' + configs.output_col_prefix + '_sentence' : row[meta_sent_key]} if configs.get_sentence_origin else {})
        }
    else:
        return {
            **{'meta_' + configs.output_col_prefix + '_confidence':max([float(row[k]) for k in confidences_keys ])},
            **({'meta_' + configs.output_col_prefix + '_sentence' : row[meta_sent_key]} if configs.get_sentence_origin else {})
        }
