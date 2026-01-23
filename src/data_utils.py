from sklearn import metrics as mt

def computeMetricsSklearnModel(
                               model,
                                dataset_train : tuple,
                                dataset_test : tuple,
                                dataset_valid : tuple) -> dict:

    '''
    returns:
        metrics :{
            accuracy    : dict['train','test','valid'], 
            precision   : dict['train','test','valid'],
            recall      : dict['train','test','valid'],
            f1_score    : dict['train','test','valid']
        }
    
    '''        
    x_train, y_train = dataset_train
    x_test,  y_test  = dataset_test
    x_valid, y_valid = dataset_valid 

    predictions_train  = model.predict(x_train)
    predictions_test   = model.predict(x_test)
    predictions_valid  = model.predict(x_valid)

    accuracies  = { 
                    'train'  : None,
                    'test'      : None,
                    'valid'     : None
                    }
    
    precisions  = {
                    'train'  : None,
                    'test'      : None,
                    'valid'     : None
    }
    recalls     = {
                    'train'  : None,
                    'test'      : None,
                    'valid'     : None}
    
    f1_scores   = {
                    'train'  : None,
                    'test'      : None,
                    'valid'     : None
    }

    auc = {
                    'train'  : None,
                    'test'      : None,
                    'valid'     : None
    }    
    

    # compute accuracy
    accuracies['train']   = mt.accuracy_score(y_train, predictions_train)
    accuracies['test']       = mt.accuracy_score(y_test, predictions_test)
    accuracies['valid']      = mt.accuracy_score(y_valid,  predictions_valid)
    
    #compute precision
    precisions['train']  = mt.precision_score(y_train, predictions_train)
    precisions['test']      = mt.precision_score(y_test, predictions_test)
    precisions['valid']     = mt.precision_score(y_valid, predictions_valid)
    
    # compute recalls
    recalls['train']     = mt.recall_score(y_train, predictions_train)
    recalls['test']         = mt.recall_score(y_test, predictions_test)
    recalls['valid']        = mt.recall_score(y_valid, predictions_valid)
    
    # compute f1_scores
    f1_scores['train']   = mt.f1_score(y_train, predictions_train)
    f1_scores['test']       = mt.f1_score(y_test, predictions_test)
    f1_scores['valid']      = mt.f1_score(y_valid, predictions_valid)

    #auc['train']   = mt.auc(y_train, predictions_train)
    #auc['test']    = mt.auc(y_test, predictions_test)
    #auc['valid']   = mt.auc(y_valid, predictions_valid)

    metrics = {
            'accuracy'  : accuracies,
            'precision' : precisions,
            'recall'    : recalls, 
            'f1_score'  : f1_scores,
            'auc'       : auc
    }

    return metrics 

