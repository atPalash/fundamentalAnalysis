import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf


class LstmPredictor:
    def __init__(self, model_save_folder_path: str, selected_stocks, selected_feature: str,
                 past_data_point_count: int = 50, debug: bool = False, debug_count: int = 5):
        self.selected_stocks = selected_stocks
        self.epochs = None
        self.train_test_ratio = None
        self.past_data_point_count = past_data_point_count
        self.selected_feature = selected_feature
        self.selected_stocks_df = None
        self.model_save_path = model_save_folder_path
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.debug = debug
        self.debug_count = debug_count

    def init_model(self, selected_stocks_df: pandas.DataFrame, train_test_ratio: float = 0.8,
                   epochs: int = 50):
        self.selected_stocks_df = selected_stocks_df
        self.train_test_ratio = train_test_ratio
        self.epochs = epochs

    def build_model(self):
        """
        This model is being trained on 80% of the data, and last 20% of data are unseen by the model. here, the entire
        dataframe is passed since we also use it for debugging and testing purpose.
        """
        model = None
        try:
            count = 0
            for stock in self.selected_stocks:
                count += 1
                if self.debug and count > self.debug_count:
                    break

                series = self.selected_stocks_df[self.selected_feature][stock]
                series = np.array(series).reshape(-1, 1)
                dataset_train = series[:int(series.shape[0] * self.train_test_ratio)]
                dataset_test = series[int(series.shape[0] * (1 - self.train_test_ratio)):]

                dataset_train = self.scaler.fit_transform(dataset_train)
                dataset_test = self.scaler.transform(dataset_test)

                x_train, y_train = self.__create_dataset(dataset_train)
                x_test, y_test = self.__create_dataset(dataset_test)

                x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
                x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

                if model is None or model.input_shape != x_train.shape[1]:
                    model = LstmPredictor.__build_neural_layer(x_train.shape[1])

                model.fit(x_train, y_train, epochs=self.epochs)
                model.save(f'{self.model_save_path}/{stock}.h5')

                # if debug:
                #     model = load_model(f'{self.model_save_path}/{stock}.h5')
                #     predictions = model.predict(x_test)
                #     predictions = self.scaler.inverse_transform(predictions)
                #     y_test_scaled = self.scaler.inverse_transform(y_test.reshape(-1, 1))
                #
                #     fig, ax = plt.subplots(figsize=(16, 8))
                #     ax.set_facecolor('#000041')
                #     ax.plot(y_test_scaled, color='red', label='Original price')
                #     plt.plot(predictions, color='cyan', label='Predicted price')
                #     plt.legend()
                #     plt.title(stock)
                #     plt.show()

        except Exception as e:
            raise

    def predict(self, current_data: pandas.DataFrame):
        """
        Predict the next stock price using current stock price.

        Arguments:
            list of current price contains past_data_point_count price data.
            current_data -> dict:
                {
                    {"stock1": list of current_price},
                    {"stock2": list of current_price},
                    {"stock3": list of current_price},
                    ...
                }
        Return:
            predictions ->
                {
                    {"stock1": prediction1},
                    {"stock2": prediction2},
                    {"stock3": prediction3},
                    ...
                }
        """

        predictions = {}
        try:
            count = 0
            for stock in self.selected_stocks:
                count += 1
                if self.debug and count > self.debug_count:
                    break
                dataset_test = current_data[self.selected_feature][stock]
                dataset_test = np.array(dataset_test).reshape(-1, 1)
                dataset_test = self.scaler.fit_transform(dataset_test)
                x_test, y_test = self.__create_dataset(dataset_test)
                x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

                model = tf.keras.models.load_model(f'{self.model_save_path}/{stock}.h5')
                prediction = model.predict(x_test)
                prediction = self.scaler.inverse_transform(prediction)
                y_test_scaled = self.scaler.inverse_transform(y_test.reshape(-1, 1))

                fig, ax = plt.subplots(figsize=(16, 8))
                ax.set_facecolor('#000041')
                ax.plot(y_test_scaled, color='red', label='Original price')
                plt.plot(prediction, color='cyan', label='Predicted price')
                plt.legend()
                plt.title(stock)
                plt.show()

                predictions[stock] = prediction
        except Exception as e:
            raise

        return predictions

    @staticmethod
    def __build_neural_layer(shape):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.LSTM(units=96, return_sequences=True, input_shape=(shape, 1)))
        model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.LSTM(units=96, return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.LSTM(units=96, return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.LSTM(units=96))
        model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.Dense(units=1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def __create_dataset(self, df):
        x = []
        y = []
        for i in range(self.past_data_point_count, df.shape[0]):
            x.append(df[i - self.past_data_point_count:i, 0])
            y.append(df[i, 0])
        x = np.array(x)
        y = np.array(y)
        return x, y