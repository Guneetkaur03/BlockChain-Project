
from libs import *
from constants import *

def model_walk_forward(history: pd.DataFrame, one_step_test: pd.DataFrame) -> np.ndarray:
    """
        This module trains a random forest classifier using expanding window

        Args:
            history (dataframe): features and labels from time 0 to t
            one_step_test (dataframe): prediction data for time t+1
        Returns:
            (array): predictions on the testing data
    """
    
    # extract features and labels
    X_train = history.drop(columns=['label']).values
    y_train = history[['label']].values
    X_test  = one_step_test.drop(columns=['label']).values
    y_test = one_step_test[['label']].values

    # feature standardization
    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    # fit model
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(X_train, y_train.ravel())
    
    # make a one-step prediction
    y_pred = model.predict(X_test)

    return y_pred


def model_evaluation(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, float, float, float]:
    """
        This module generates all the evaluation metrics for the model trained
        and returns the metric values
        Args:
            y_true (array): containing true labels
            y_pred (array): containing predicted labels
        Returns:
            (tuple): precision, recall, accuracy, f1_scores
    """

    precision = precision_score(y_true, y_pred, average='weighted')
    recall    = recall_score(y_pred, y_pred, average='weighted')
    accuracy  = accuracy_score(y_true, y_pred)
    f1_scores = f1_score(y_true, y_pred, average='weighted')

    print("\nClassification Report")
    print(classification_report(y_true, y_pred, labels=[0,1]))

    # create confusion matrix and its plot
    plt.figure(figsize=(20, 10))
    ax = sns.heatmap(confusion_matrix(y_true, y_pred), annot=True)
    plt.savefig(PLOTS + 'confusion-matrix.png')

    return precision, recall, accuracy, f1_scores


def model_training(df: pd.DataFrame) -> None:
    """
        This module creates expanding windows and
        train walk forward model

        Args:
            df (dataframe): yearly comined dataframe
        Returns:
            (None)
    """

    predictions = []
    actual = []

    # accuracy scores
    testing_accuracy = []

    print("\nTraining model")
    for t in tqdm(range(1, len(set(df.index)))):
    
        # creating temporal windows for training and testing
        history = df.loc[0:t]
        one_step_test = df.loc[t+1]
        
        y_pred = model_walk_forward(history, one_step_test)

        testing_accuracy.append(accuracy_score(one_step_test[['label']].values, y_pred))

        actual.extend(one_step_test[['label']].values)
        predictions.extend(y_pred)

        logging.info('step 3.2.1 - Trained on batch 0 to {} and Tested on {} batch'.format(t, t+1))

        # get evaluation metrics
        precision, recall, accuracy, f1_scores = model_evaluation(actual, predictions)

        if t % 10 == 0:
            # log the model scores
            logging.info('step 3.2.1 Precision is {}'.format(precision))
            logging.info('step 3.2.1 Recall is {}'.format(recall))
            logging.info('step 3.2.1 Accuracy is {}'.format(accuracy))
            logging.info('step 3.2.1 f1_score is {}'.format(f1_scores))

            # also print them
            print('Precision is {}'.format(precision))
            print('Recall is {}'.format(recall))
            print('Accuracy is {}'.format(accuracy))
            print('f1_score is {}'.format(f1_scores))

        # plot precision-recall graph
        precision, recall, _ = precision_recall_curve(actual, predictions)
        disp = PrecisionRecallDisplay(precision=precision, recall=recall)
        disp.plot()
        plt.savefig(PLOTS + 'pr.png')

        # plot step wise accuracy
        plt.figure(figsize=(20, 10))
        plt.plot(np.arange(t), testing_accuracy, 'b', marker='o', markevery=1, label='Testing Accuracy')
        plt.title('t+1 step testing accuracy')
        plt.xlabel('steps')
        plt.ylabel('accuracy')
        plt.grid(True)
        plt.legend()
        plt.savefig(PLOTS + 'accuracy.png')


        plt.close("all")